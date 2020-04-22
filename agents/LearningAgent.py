import random
import tensorflow as tf
# The following 3 lines of code are needed to permit TensorFlow to expand GPU memory
# usage while running.
config = tf.compat.v1.ConfigProto()
config.gpu_options.allow_growth = True
session = tf.compat.v1.Session(config=config)
# I suspect there exists a setting within TensorFlow to enable this behavior by default
# but my searching has not yet found it.
#from keras.optimizers import Adam
from tensorflow.keras.optimizers import Adam
from keras.models import load_model
#import keras
import tensorflow.keras as keras # NOT the same as import keras!!
import glob2
import pickle
import random
import copy
import sys
import numpy as np
from enums import *
from contextlib import ExitStack

# what are we computing loss against?
# seperate training from running?
# different networks for different tasks? playing cards, predicting partners, making calls
# Qt+1(st,at)=Qt(st,at)+αt[rt+1+γmaxaQ(st+1,a)−Qt(st,at)]

# TODO Modify to fit our needs. This is mostly copied in to serve as a framework that we can learn from.
# Code transcribed from https://www.youtube.com/watch?v=CoePrz751lg
# github repo at https://github.com/philtabor/Youtube-Code-Repository
# NOTE: It's currently feeling like there's two major issues complicating our adaption of this
# code base to our desired behavior:
#       1. The exact behavior of the OpenAI gym make evn. has not been established
#       2. We can't be sure that we're running the same version of tensorflow/keras as orginal code
#           2a. This seems like a non-issue since I can get the sample code running if cloned from the given repo.

class DuelingDeepQNetwork(keras.Model):
    # ^This is creating a custom model that will have the dueling deep Q behavior built into it
    def __init__(self, n_actions, fc1_dims, fc2_dims): #TODO consider having this take the input dims as well
        super(DuelingDeepQNetwork, self).__init__()
        # ^Do the keras.Model init
        self._valid_play_list = [1 for i in range(8)]
        self.dense1 = keras.layers.Dense(fc1_dims, activation="relu")
        # ^Add a first densely connected layer, I think this is the input layer, though it might actually not be
        self.dense2 = keras.layers.Dense(fc2_dims, activation="relu")
        # ^add a second dense layer, this should be a hidden layer within the network
        self.V = keras.layers.Dense(1, activation=None)
        # This looks to be a "value" layer that compresses the output of the network to a single value
        #We use the sigmoid function to force all of the values contained within actions to be between 0 and 1.
        self.A = keras.layers.Dense(n_actions, activation='sigmoid') # NOTE since this is activation=None the output can be -1 to 1, I think
        #TODO Consider adding the filtering layer into this network init
        # This is the layer that the action to be taken will be selected from
        # The way the call method below looks to work the values of the 2nd layer
        # feed into both the V and A layer
        # NOTE: Copied from https://github.com/tensorflow/tensorflow/issues/34199

    def set_valid_play_list(self, a_valid_play_list):
        self._valid_play_list = a_valid_play_list

    def call(self, state):
        
        # I'm inclined to think that the state should be thought of as the input layer
        x = self.dense1(state)
        # dense1 would then be the 1st hidden layer
        x = self.dense2(x)
        # dense2 the second hidden layer
        V = self.V(x)
        # V is the singular value layer
        A = self.A(x)
        # and A is the action output layer
#        self.outputs = A
#        tf.print(self.outputs)
        Q = (V + (A - tf.reduce_mean(A, axis=1, keepdims=True)))
        # The Q value is calculated by the above formula
        return Q

    def advantage(self, state):
        x = self.dense1(state)
        x = self.dense2(x)
        A = self.A(x)
        #By performing an element wise multiplication between actions and the valid play list, we can 
        #ensure that the action chosen is a valid action. 
        actions = tf.math.multiply(A, self._valid_play_list)
        # here A is collection of advantages gained through each action-state transition
        # I've referenced A as the action layer elsewhere, that's slightly inacurate I think
        return actions


#    def compute_output_shape(self, input_shape):
        #Within keras.engine.base_layer, the following behavior was observed:

        #Computes the output shape given an input.
        #Input = Shape tuple (tuple of integers)
                #or list of shape tuples (one per output tensor of the layer).
                #Shape tuples can include None for free dimensions,
                #instead of an integer.
        #Output = An output shape tuple.
#        return (input_shape[0],self.layers[-1].units)
        #return input_shape

class ReplayBuffer():
    # This class is used to hold onto action-state collections and the reward associated with that transition
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
        # This is where the actual storing of action-state transitions is done
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
    # This should be the actual agent that is making the decisions
    def __init__(self, lr, gamma, n_actions, epsilon, batch_size,
                    input_dims, epsilon_dec=1e-3, epsilon_min=1e-3,
                    mem_size=100000, fname='dueling_dqn.h5', fc1_dims=128,
                    fc2_dims=128, replace=100):
        self.score = 0
        # The action_space is the number of possible actions, for us I think this should be 8?
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
        # q_eval is the network that will look across the current state of the game to make a prediction
        self.q_eval = DuelingDeepQNetwork(n_actions, fc1_dims, fc2_dims)
        # q_next is the "target network that we use the generate the values for the cost function"
        # TODO get a better understanding of what that means; https://youtu.be/CoePrz751lg?t=1305
        self.q_next = DuelingDeepQNetwork(n_actions, fc1_dims, fc2_dims)
        # TODO I think this preps the network for use, but don't really know for sure
        self.q_eval.compile(optimizer=Adam(learning_rate=lr), loss='mean_squared_error')
        # this is just needed to make it work? don't really know why, the video didn't go into much depth here
        self.q_next.compile(optimizer=Adam(learning_rate=lr), loss='mean_squared_error')
        dummy_state = np.ones((1,1228), dtype=np.float32)

        self.q_eval.advantage(dummy_state)
        self.q_next.advantage(dummy_state)
        self.load_model()

    def store_transition(self, state, action, reward, new_state, done):
        self.memory.store_transition(state, action, reward, new_state, done)

    def set_valid_play_lists(self, a_valid_play_list):
        self.q_next.set_valid_play_list(a_valid_play_list)
        self.q_eval.set_valid_play_list(a_valid_play_list)

    # This play_card method is code we wrote to serve as an interface between the imported code and our existing code base
    def play_card(self, a_player, a_game):

        self._valid_indices_list = [index for index in range(len(a_player.get_valid_play_list())) if a_player.get_valid_play_list()[index] != False]
#        self._valid_play_list = tf.convert_to_tensor(a_player.get_valid_play_list(), dtype=tf.float32)
        self.set_valid_play_lists(tf.convert_to_tensor(a_player.get_valid_play_list(), dtype=tf.float32))
        observation = a_game.get_game_state_for_player(a_player.get_player_id())
        action = self.choose_action(observation)
#        print(f"Action is: {type(action)}")
#        print(f"Action is: {type(np.int64())}")
        if type(action) != type(np.int64()): # This check is needed because our game can have a single action outcome
            observation_, reward, done = a_game.handle_action_for_player(action[0], a_player) #Currently shooting for the end of every trick.
        else:
            observation_, reward, done = a_game.handle_action_for_player(action, a_player) #Currently shooting for the end of every trick.
        #self.score += reward
        self.store_transition(observation, action, reward, observation_, done) #This stores the result observation from the action. We aren't doing this yet either.
        observation = observation_ #The game's observation is reset to the observation after a specific action has been made and the env has been stepped.
        self.learn() #Updates the weights of the network?


    def choose_action(self, observation):
        if np.random.random() < self.epsilon:
        # The agent should take a random action some % of the time to continue exploring
            action = np.random.choice(self._valid_indices_list)
        else:
        # Here is where the agent looks across the set of advantages and selects the highest one
            #For unknown reasons, we have to convert this to a tensor rather than a numpy array. (Research at future date)
            state = tf.convert_to_tensor(observation) 
            actions = self.q_eval.advantage(state)
            test = self.q_next.advantage(state)

            #argmax returns the index of the largest element in the tensor.
            action = tf.math.argmax(actions, axis=-1).numpy()[0]
            #We eval so we can actually get the value out of the tensor. For unknown reasons, we have to use
            #keras.backend.eval rather than tf.keras.backend.eval. We will research this at a later date.
#            action = keras.backend.eval(action)
        return action

    def make_call(self, a_player):#TODO Expanded this method
        # Take in a list of 32 numbers, 1's where the hand has that card
        # have some hidden layers
        # filter for valid calls
        # output argmax(an 8 element output layer)
        return Calls.none.value

    def learn(self):
        if self.memory.mem_cntr < self.batch_size:
            return # TODO this might be good place for file reading
        
        if self.learn_step_counter % self.replace == 0:
            # If replace many learning actions have been taken since the last time the
            # target network was updated, then update the target network
            # https://youtu.be/CoePrz751lg?t=1594
            
            self.q_next.set_weights(self.q_eval.get_weights())
            self.save_model()

        # the \ on the next line just lets python know that the line continues on the next line
        # TODO we might actually want to consier using the \ in other places in our code
        states, actions, rewards, states_, dones = \
                                            self.memory.sample_buffer(self.batch_size)
        # Pull in information about a game from the buffer

        # TODO Don't quite know what this is doing
#        print(f"Inputs is: {self.q_eval.inputs}")
#        print(f"Outputs is: {self.q_eval.outputs}")
        states = tf.convert_to_tensor(states) #TODO Consider making a copy of states, since 2 places expect 2 different behaviors
        q_pred = self.q_eval(states)
        # This gets the value of the max future action
        states_ = tf.convert_to_tensor(states_)
        q_next = tf.math.reduce_max(self.q_next(states_), axis=1, keepdims=True)
#        q_next = keras.backend.eval(q_next)
        # need to copy the prediction network because of the way keras handles calculating loss
        # https://youtu.be/CoePrz751lg?t=1698
        q_pred = keras.backend.eval(q_pred)
        q_target = np.copy(q_pred)
        # NOTE: I don't like the naming here since there's a target network in use that's called next,
        # then we get this copied network that's called target. This seems confusing.

        #room for improvement here?
        q_next = keras.backend.eval(q_next)
        for index, terminal in enumerate(dones):
            if terminal:
                # terminal indicates that we've reached the end of a game, and as such
                # the future reward must be 0
                q_next[index] = 0.0
            # https://youtu.be/CoePrz751lg?t=1819
            q_target[index, actions[index]] = rewards[index] + self.gamma*q_next[index]
        # TODO: Not really sure what this is doing
        states = keras.backend.eval(states)
        self.q_eval.train_on_batch(states, q_target)
        # decrement the epsilon value, make plays less randomly as tranining progresses
        self.epsilon = self.epsilon - self.epsilon_dec if self.epsilon > \
                        self.epsilon_min else self.epsilon_min
        # Increment the counter of how many training runs have been done
        self.learn_step_counter += 1

    def save_model(self):
        eval_path = "eval_" + self.fname
        self.q_eval.save_weights(eval_path)
        next_path = "next_" + self.fname
        self.q_next.save_weights(next_path)

    def load_model(self):
        eval_path = "eval_" + self.fname
        self.q_eval.save_weights(eval_path)
        next_path = "next_" + self.fname
        self.q_next.load_weights(next_path)

# ^NOTE: This is the end of the transcribed sample code, I'm sure there's was we can modify it to suit our needs.
        
# Code spiking group file read