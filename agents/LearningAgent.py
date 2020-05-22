import random
import tensorflow as tf
# The following 3 lines of code are needed to permit TensorFlow to expand GPU memory
# usage while running.
config = tf.compat.v1.ConfigProto()
config.gpu_options.allow_growth = True
session = tf.compat.v1.Session(config=config)
# I suspect there exists a setting within TensorFlow to enable this behavior by default
# but my searching has not yet found it.
from tensorflow.keras.optimizers import Adam # pylint: disable=import-error 
from keras.models import load_model
import tensorflow.keras as keras # NOT the same as import keras!! pylint: disable=import-error
import random
import os
import numpy as np
import math
from enums import Calls

# Code transcribed from https://www.youtube.com/watch?v=CoePrz751lg
# github repo at https://github.com/philtabor/Youtube-Code-Repository

class DuelingDeepQNetwork(keras.Model):
    '''
    # This is creating a custom model that will have the dueling deep Q behavior built into it
    '''
    def __init__(self, n_actions, fc1_dims, fc2_dims, fc3_dims, fc4_dims, fc5_dims, fc6_dims): 
        super(DuelingDeepQNetwork, self).__init__()
        # ^Do the keras.Model init
        self._valid_actions_filter = [1 for i in range(8)]
        self.dense1 = keras.layers.Dense(fc1_dims, activation="selu")
        self.dense2 = keras.layers.Dense(fc2_dims, activation="selu")
        self.dense3 = keras.layers.Dense(fc3_dims, activation="selu")
        self.dense4 = keras.layers.Dense(fc4_dims, activation="selu")
        self.dense5 = keras.layers.Dense(fc5_dims, activation="selu")
        self.dense6 = keras.layers.Dense(fc6_dims, activation="selu")
        self.V = keras.layers.Dense(1, activation=None)
        # This looks to be a "value" layer that compresses the output of the network to a single value
        # We use the softplus function to force all of the values contained within actions are > 0.
        self.A = keras.layers.Dense(n_actions, activation='softplus')
        # This is the layer that the action to be taken will be selected from
        # The way the call method below looks to work the values of the 2nd layer
        # feed into both the V and A layer

    def set_valid_actions_filter(self, a_valid_actions_filter):
        self._valid_actions_filter = a_valid_actions_filter

    def call(self, state):
        # State should be thought of as the input
        x = self.dense1(state)
        x = self.dense2(x)
        x = self.dense3(x)
        x = self.dense4(x)
        x = self.dense5(x)
        x = self.dense6(x)
        V = self.V(x)
        # V is the singular value layer
        A = self.A(x)
        A = tf.math.multiply(A, self._valid_actions_filter)
        A = tf.math.add(A, self._valid_actions_filter)
        # and A is the action output layer
        Q = (V + (A - tf.reduce_mean(A, axis=1, keepdims=True)))
        return Q

    def advantage(self, state):
        x = self.dense1(state)
        x = self.dense2(x)
        x = self.dense3(x)
        x = self.dense4(x)
        x = self.dense5(x)
        x = self.dense6(x)
        A = self.A(x)
        #By performing an element wise multiplication between actions and the valid play list, we can
        #ensure that the action chosen is a valid action.
        actions = tf.math.multiply(A, self._valid_actions_filter)
        #Multiplication alone was insufficient, addition was also required
        #because all valid cards could potentially have a value of 0 within actions.
        actions = tf.math.add(actions, self._valid_actions_filter)
        return actions

class ReplayBuffer():
    '''
    This class is used to hold onto action-state collections and the reward associated with that transition
    '''
    def __init__(self, max_size, input_shape):
        self.mem_size = max_size
        self.mem_cntr = 0
        self.state_memory = np.zeros((self.mem_size, *input_shape),
                                        dtype=np.float32)
        self.new_state_memory = np.zeros((self.mem_size, *input_shape), dtype=np.float32)
        self.action_memory = np.zeros(self.mem_size, dtype=np.int32)
        self.reward_memory = np.zeros(self.mem_size, dtype=np.float32)
        self.terminal_memory = np.zeros(self.mem_size, dtype=np.bool)

    def store_transition(self, state, action, reward, state_, done):
        index = self.mem_cntr % self.mem_size
        self.state_memory[index] = state
        self.new_state_memory[index] = state_
        self.action_memory[index] = action
        self.reward_memory[index] = reward
        self.terminal_memory[index] = done
        self.mem_cntr += 1

    def sample_buffer(self, batch_size):
        # This will pull a batch of random transitions from the buffer for training
        max_mem = min(self.mem_cntr, self.mem_size)
        batch = np.random.choice(max_mem, batch_size, replace=False)
        states = self.state_memory[batch]
        new_states = self.new_state_memory[batch]
        actions = self.action_memory[batch]
        rewards = self.reward_memory[batch]
        dones = self.terminal_memory[batch]
        return states, actions, rewards, new_states, dones

class Agent():
    '''
    This should be the actual agent that is making the decisions
    '''
    def __init__(self, lr=1e-7, gamma=.55, n_actions=8, epsilon=.99, batch_size=64,
                    input_dims=[1228], epsilon_dec=1e-4, epsilon_min=1e-3,
                    mem_size=100000, fname='dueling_dqn.h5', fc1_dims=1228,
                    fc2_dims=1228, fc3_dims=1228, fc4_dims=1024, fc5_dims=512, fc6_dims=256, replace=500):
        self.score = 0
        # The action_space is the number of possible actions, for us this is 8
        self.action_space = [i for i in range(n_actions)]
        # gamma is the future discount factor, the more distant a reward is in the future the less influence it should have now
        self.gamma = gamma
        # Epsilon is the % likelyhood of taking a random action rather than the precived best action
        self.epsilon = epsilon
        # Epsilon_dec is how quickly epslion decrements toward some minimum value
        self.epsilon_dec = epsilon_dec
        # Epsilon_min is the smallest value epsilon will reach
        self.epsilon_min = epsilon_min
        # fname is the name of the file used to store the networks weights
        self.fname = fname
        # replace is the number of training runs to be performed before the target network is updated
        # to the current prediction network
        self.replace = replace
        # batch_size is the amount of games to be loaded into memory for training at a time
        self.batch_size = batch_size
        # learn_step_counter is the number of training runs done so far
        self.learn_step_counter = 0
        # memory is the buffer into which action-state transitions will be stored
        self.memory = ReplayBuffer(mem_size, input_dims)
        self._last_seen_state = None
        self._last_taken_action = None
        self.__trump_strengths = [3.5, 3.25, 3.2, 3, 2.8, 2, 1.5, 1.25, 1.1, 1.25, 0.95, 0.8, 0.65, 0.65, 0.65]
        self.__fail_strengths = [3, 0.25, 0.1, 0.02, 0.02, 0.02]
        self._trump_strength = 100
        self._clubs_strength = 100
        self._spades_strength = 100
        self._hearts_strength = 100
        self._total_strength = 0
        self.call_generator_trained = False
        self._valid_call_list = tf.convert_to_tensor([0 for i in range(8)])
        self.call_memory = ReplayBuffer(mem_size, [32])
        # q_eval is the network that will look across the current state of the game to make a prediction
        self.q_eval = DuelingDeepQNetwork(n_actions, fc1_dims, fc2_dims, fc3_dims, fc4_dims, fc5_dims, fc6_dims)
        # q_next is the "target network that we use the generate the values for the cost function"
        self.q_next = DuelingDeepQNetwork(n_actions, fc1_dims, fc2_dims, fc3_dims, fc4_dims, fc5_dims, fc6_dims)
        self.call_generator = DuelingDeepQNetwork(n_actions=8,fc1_dims=32,fc2_dims=8,fc3_dims=8, fc4_dims=8, fc5_dims=8, fc6_dims=4)
        self.score_predictor = DuelingDeepQNetwork(n_actions=8,fc1_dims=32,fc2_dims=8,fc3_dims=8, fc4_dims=8, fc5_dims=8, fc6_dims=4)
#        self.call_generator = tf.keras.models.Sequential([keras.layers.Dense(32),
#                                                        keras.layers.Dense(16, activation='relu'),
#                                                        keras.layers.Dense(8, activation='sigmoid')])
        '''
        input1 = keras.layers.Input(shape=(32,))
        y1 = keras.layers.Dense(32, activation='relu')(input1)
        x1 = keras.layers.Dense(8, activation='relu')(y1)
        input2 = keras.layers.Input(shape=(8,))
        x2 = keras.layers.Dense(8, activation='relu')(input2)
        Multiply = keras.layers.Multiply()([x1, input2])
        out = keras.layers.Dense(8)(Multiply)
        model = keras.models.Model(inputs=[input1, input2], outputs=out)
        self.call_generator = model
        call_options = keras.layers.Input(shape=(8,))
        temp2 = keras.layers.Dense(8, activation='sigmoid')(call_options)
        cards = keras.layers.Input(shape=(32,))
        temp = keras.layers.Dense(16, activation='relu')(cards)
        temp = keras.layers.Dense(8, activation='relu')(cards)
        multi = keras.layers.Multiply()([temp, temp2])
        out = keras.layers.Dense(8)(multi)
        self.call_generator = keras.models.Model(inputs=[cards, call_options], outputs=out)
        '''

        self.call_generator.compile(optimizer=Adam(learning_rate=lr), loss='mean_squared_error')
        self.score_predictor.compile(optimizer=Adam(learning_rate=lr), loss='mean_squared_error')
        self.q_eval.compile(optimizer=Adam(learning_rate=lr), loss='mean_squared_error')
        self.q_next.compile(optimizer=Adam(learning_rate=lr), loss='mean_squared_error')

        try:
            dummy_state = np.ones((1,1228), dtype=np.float32)
            self.q_eval.advantage(dummy_state)
            self.q_eval(dummy_state)
            self.q_next.advantage(dummy_state)
            self.q_next(dummy_state)
            self.load_model()
        except:
            print("Falied to load the networks")

    def store_transition(self, state, action, reward, new_state, done):
        self.memory.store_transition(state, action, reward, new_state, done)

    def store_call_mem_transition(self, state, action, reward):
        self.call_memory.store_transition(state, action, reward, None, True)

    def set_valid_play_lists(self, a_valid_play_list):
        self.q_next.set_valid_actions_filter(a_valid_play_list)
        self.q_eval.set_valid_actions_filter(a_valid_play_list)

    # This play_card method is code we wrote to serve as an interface between the imported code and our existing code base
    def play_card(self, a_player, a_game):
        self._valid_indices_list = [index for index in range(len(a_player.get_valid_play_list())) if a_player.get_valid_play_list()[index] != False]
        self.set_valid_play_lists(tf.convert_to_tensor(a_player.get_valid_play_list(), dtype=tf.float32))
        observation = a_game.get_game_state_for_player(a_player.get_player_id())
        action = self.choose_action(observation)
        # The following two lines were added in to store this information so we can decouple
        # the learn method from the play_card method. So now learn can just be called by the player
        # at the end of the trick.
        self._last_seen_state = observation
        self._last_taken_action = action

        return action

    def choose_action(self, observation):
        if np.random.random() < self.epsilon:
        # The agent should take a random action some % of the time to continue exploring
            action = np.random.choice(self._valid_indices_list)
        else:
        # Here is where the agent looks across the set of advantages and selects the highest one
            state = np.array(observation)
            actions = self.q_eval.advantage(state)
            _ = self.q_next.advantage(state)
            #argmax returns the index of the largest element in the tensor.
            action = tf.math.argmax(actions, axis=-1).numpy()[0]
        return action

    def make_call(self, a_player):
        return self.make_call_custom(a_player)

    def __reset_default_strengths(self):
        self._trump_strength = 100
        self._clubs_strength = 100
        self._spades_strength = 100
        self._hearts_strength = 100
        self._total_strength = 0

    def gauge_hand_strength(self, a_hand):
        for card in a_hand.get_cards_in_hand():
            if card.get_card_suit() == "trump":
                self._trump_strength *= self.__trump_strengths[card.get_card_rank()]
            elif card.get_card_suit() == "clubs":
                self._clubs_strength *= self.__fail_strengths[card.get_card_rank() - 9]
            elif card.get_card_suit() == "spades":
                self._spades_strength *= self.__fail_strengths[card.get_card_rank() - 9]
            elif card.get_card_suit() == "hearts":
                self._hearts_strength *= self.__fail_strengths[card.get_card_rank() - 9]
        self._total_strength = self._trump_strength + self._clubs_strength + self._spades_strength + self._hearts_strength

    def find_best_callable_ace_suit(self, a_player):
        fail_strengths =[self._clubs_strength, self._spades_strength, self._hearts_strength]
        callable_strengths = []
        for i in range(3):
            callable_strengths.append(fail_strengths[i] * a_player.get_valid_call_list()[i+1])
        return 1 + callable_strengths.index(max(callable_strengths))

    def make_call_custom(self, a_player):
        call_index = -1
        self.gauge_hand_strength(a_player.get_hand())
        if self._total_strength > 42000:
            call_index = Calls.zolo_s_s.value
        elif self._total_strength > 28000:
            call_index = Calls.zolo_s.value
        elif self._total_strength > 9000:
            call_index = Calls.zolo.value
        elif self._total_strength < 2500 and a_player.get_valid_call_list()[Calls.first_trick.value] == 1:
            call_index = Calls.first_trick.value
        elif self._total_strength < 2300 and sum(a_player.get_valid_call_list()[Calls.ace_clubs.value:Calls.ace_hearts.value]) > 0: # the second condition means this block is only entered if an ace is callable
            call_index = self.find_best_callable_ace_suit(a_player)
        else:
            call_index = Calls.none.value
        self.__reset_default_strengths()
        return call_index

    def make_call_using_learning(self, a_player):
        # Generate a list of 32 numbers, 1's where the hand has that card
        valid_call_tensor = tf.reshape(tf.convert_to_tensor(a_player.get_valid_call_list(), dtype=tf.float32), (1,8))
        self.call_generator.set_valid_actions_filter(valid_call_tensor)
        card_list = [0 for i in range(32)]
        for card in a_player.get_cards_in_hand():
            card_list[card.get_card_id()] = 1
        card_list = tf.reshape(tf.convert_to_tensor(card_list, dtype=tf.float32),(1,32))
        self.players_starting_card_list = card_list
        # NOTE: When any other player has made a solo call don't learn from that round
        #   This is to avoid strengthing the connection between a hand state and no call
        #   when another player made a bad call.
        # NOTE: Expressed concern about associating good hands with hard calls
        #   The no call could get over-reinforced?

        call_weights = self.call_generator.advantage(card_list)
        call = tf.math.argmax(call_weights, axis=-1).numpy()[0]
        # NOTE: New insight the call generator seems to get 'stuck' into call states, it either
        # makes many high calls in a game, or it makes mostly 0 calls for a game.
        # This could mean that we're not reinfocing the behavior the way we want to be.
        print(f"Called: {call}")
        return call

#    def train_call_generator(self):
#        if self.call_memory.mem_cntr < self.batch_size:
#           return

#        if self.learn_step_counter % (self.replace * 8) == 0:
#            self.score_predictor.set_weights(self.call_generator.get_weights())

#        states, actions, rewards, states_, dones = \
#                        self.call_memory.sample_buffer(self.batch_size)

#        call_targets = [[0 for i in range(8)] for i in range(self.batch_size)]
#        for index, reward in enumerate(rewards):
#            action = actions[index]
#            if reward > 0:
#                for i in range(8):
#                    if i >= action:
#                        call_targets[index][i] = reward/(reward*(i-action+1))
                #   If reward is positive, skew towards action, and slightly toward the higher calls?
#            else:
#                for i in range(8):
#                    call_targets[index][i] = (-i + action - 2) * (1/(8 - action))
                #   If reward is negative, skew away from the call made, which is the action
#        call_targets = np.array(call_targets)
#        self.call_generator.train_on_batch(states, call_targets)
#        self.call_generator_trained = True

    def learn(self, a_player, a_game):
        observation_, reward, done = a_game.get_updated_game_state_for_player(a_player)
        self.store_transition(self._last_seen_state, self._last_taken_action, reward, observation_, done)
        if self.memory.mem_cntr < self.batch_size:
            return

        if self.learn_step_counter % self.replace == 0:
            # If replace many learning actions have been taken since the last time the
            # target network was updated, then update the target network
            # https://youtu.be/CoePrz751lg?t=1594
            dummy_state = np.ones((1,1228), dtype=np.float32)
            _ = self.q_next(dummy_state)
            _ = self.q_next.advantage(dummy_state)
            self.q_next.set_weights(self.q_eval.get_weights())
            self.save_model()

        states, actions, rewards, states_, dones = \
                                            self.memory.sample_buffer(self.batch_size)
        q_pred = self.q_eval(states)
        # This gets the value of the max future action
        q_next = tf.math.reduce_max(self.q_next(states_), axis=1, keepdims=True)
        # need to copy the prediction network because of the way keras handles calculating loss
        # https://youtu.be/CoePrz751lg?t=1698
        q_target = np.copy(q_pred)
        q_next = np.array(q_next)
        for index, terminal in enumerate(dones):
            if terminal:
                # terminal indicates that we've reached the end of a game, and as such
                # the future reward must be 0
                q_next[index] = 0.0
            q_target[index, actions[index]] = rewards[index] + self.gamma*q_next[index]
        self.q_eval.train_on_batch(states, q_target)
        # decrement the epsilon value, make plays less randomly as tranining progresses
        self.epsilon = self.epsilon - self.epsilon_dec if self.epsilon > \
                        self.epsilon_min else self.epsilon_min
        self.learn_step_counter += 1

    def save_model(self):
        eval_path = "eval_" + self.fname
        self.q_eval.save_weights(eval_path)
        next_path = "next_" + self.fname
        self.q_next.save_weights(next_path)
        call_path = "call_" + self.fname
        if self.call_generator_trained:
            self.call_generator.save_weights(call_path)

    def load_model(self):
        self.epsilon = 0.1
        try:
            eval_path = "eval_" + self.fname
            self.q_eval.load_weights(eval_path)
        except:
            print("Couldn't load weights for the eval network")
        try:
            next_path = "next_" + self.fname
            self.q_next.load_weights(next_path)
        except:
            print("Couldn't load weights for the next network")
#        try:
#            call_path = "call_" + self.fname
#            self.call_generator.load_weights(call_path)
#        except:
#            print("Couldn't load weights for the call generator")