import random
import tensorflow as tf
from keras.optimizers import Adam
from keras.models import load_model
import keras
import glob2
import pickle
import random
import numpy as np
from contextlib import ExitStack

# what are we computing loss against?
# seperate training from running
# different networks for different tasks? playing cards, predicting partners, making calls
# Qt+1(st,at)=Qt(st,at)+αt[rt+1+γmaxaQ(st+1,a)−Qt(st,at)]

# TODO Modify to fit our needs. This is mostly copied in to serve as a framework that we can learn from.
# Code transcribed from https://www.youtube.com/watch?v=CoePrz751lg
class DuelingDeepQNetwork(keras.Model):
    # ^This is creating a custom model that will have the dueling deep Q behavior built into it
    def __init__(self, n_actions, fc1_dims, fc2_dims):
        super(DuelingDeepQNetwork, self).__init__()
        # ^Do the keras.Model init
        self.dense1 = keras.layers.Dense(fc1_dims, activation="relu")
        # ^Add a first densely connected layer, I think this is the input layer, though it might actually not be
        self.dense2 = keras.layers.Dense(fc2_dims, activation="relu")
        # ^add a second dense layer, this should be a hidden layer within the network
        self.V = keras.layers.Dense(1, activation=None)
        # This looks to be a "value" layer that compresses the output of the network to a single value
        self.A = keras.layers.Dense(n_actions, activation=None)
        # This is the layer that the action to be taken will be selected from
        # The way the call method below looks to work the values of the 2nd layer
        # feed into both the V and A layer

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

        Q = (V + (A - tf.reduce_mean(A, axis=1, keepdims=True)))
        # The Q value is calculated by the above formula
        return Q

    def advantage(self, state):
        x = self.dense1(state)
        x = self.dense2(x)
        A = self.A(x)
        # here A is collection of advantages gained through each action-state transition
        # I've referenced A as the action layer elsewhere, that's slightly inacurate I think
        return A

class ReplayBuffer():
    #This is confisung to me. Might need some more explanation. AD
    # This class is used to hold onto action-state collections and the reward associated with that transition
    def __init__(self, max_size, input_shape):
        self.mem_size = max_size
        self.mem_cntr = 0
        # 
        self.state_memory = np.zeros((self.mem_size, *input_shape),
                                        dtype=np.float32)
        self.new_state_memory = np.zeros((self.mem_size, *input_shape),
                                        dtype=np.float32)
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
    #I think we should go through and discuss this in person so we know we both understand. AD
    def __init__(self, lr, gamma, n_actions, epsilon, batch_size,
                    input_dims, epsilon_dec=1e-3, epsilon_min=1e-3,
                    mem_size=100000, fname='dueling_dqn.h5', fc1_dims=128, # TODO The dims need to be changed
                    fc2_dims=128, replace=500):
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
        # learn_step_counter is the number of training runs done so far TODO make sure this is correct
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

    def store_transition(self, state, action, reward, new_state, done):
        self.memory.store_transition(state, action, reward, new_state, done)

    def choose_action(self, observation):
        if np.random.random() < self.epsilon:
        # The agent should take a random action some % of the time to continue exploring
            action = np.random.choice(self.action_space)
        else:
        # Here is where the agent looks across the set of advantages and selects the highest one
            state = np.array([observation])
            actions = self.q_eval.advantage(state)
            # TODO Filter the actions based on the valid play list
            # actions is expected to be 8 elements in size
            # the valid play list is also 8 elements in size
            # if we do an elementwise multiplication of each
            # the result should be filtered?
            # This is assuming that the action values are positive!
            action = tf.math.argmax(actions, axis=1).numpy()[0]

        return action

    def play_card(self, a_player, a_game):
        # NOTE: To make sure that a card is valid to play we can prefliter the cards in hand by the
        # valid play list

        # We want:
        #   The cards in hand, (This would be a 32 element list) DONE?
        #   The cards played to the trick so far, (4*32 element list) Done?
        #   The players potential partners list, (4 element list) Done?
        #   The list of cards played so far, (4*8*32 elements) Done?
        #   The call state of the game, (This would be a 4*8 element list)
        #   The normalized list of points taken by each player (4 elements) NOTE: [pl_1_points, pl_2_points...]
        #   The normailzed score list for each player (4 elements) NOTE: handle the same way as points
        #   32 + 4*32  + 4 + 4*8*32 + 4*8 + 4 + 4 = 1228

        current_round = a_game.get_round()
        game_state_for_player = current_round.get_game_state_for_player(a_player.get_player_id())
        game_state = []
        poorly_named_cards_in_hand_list = [0 for i in range(32)]
        valid_indices_list = [index for index in range(len(a_player.get_valid_play_list())) if a_player.get_valid_play_list()[index] != 0]
        cards_in_hand = a_player.get_cards_in_hand()
        #   get the id of the card at each valid index
        #   at that id set the value of poorly_named_cards_in_hand_list to 1
        for index in valid_indices_list:
            poorly_named_cards_in_hand_list[cards_in_hand[index].get_card_id()] = 1
        game_state.append(tf.keras.backend.flatten(tf.constant(poorly_named_cards_in_hand_list)))

        current_trick = game_state_for_player["current_trick"]
        cards_played_to_trick = current_trick.get_played_cards_list()
        poorly_named_list_of_cards_played_to_trick = np.zeros((4,32), dtype=np.int8)
        for card in cards_played_to_trick:
            if card is not None:
                poorly_named_list_of_cards_played_to_trick[card.get_owning_player()][card.get_card_id()] = 1
        game_state.append(tf.keras.backend.flatten(tf.constant(poorly_named_list_of_cards_played_to_trick)))

        game_state.append(tf.keras.backend.flatten(tf.constant(a_player.get_potential_partners_list())))

        game_state.append(tf.keras.backend.flatten(tf.constant(game_state_for_player["trick_history"])))

        game_state.append(tf.keras.backend.flatten(tf.constant(game_state_for_player["call_matrix"])))

        normalized_player_point_list = [player.get_round_points()/120 for player in a_game.get_players_list()]
        game_state.append(tf.keras.backend.flatten(tf.constant(normalized_player_point_list)))

        normalized_player_score_list = [player.get_total_score()/120 for player in a_game.get_players_list()]
        game_state.append(tf.keras.backend.flatten(tf.constant(normalized_player_score_list)))
        game_state = tf.keras.backend.flatten(tf.constant(game_state))
        # ^In theory game_state is now a 1228 element long tensor?
        
        card_to_play_index = self.choose_action(game_state)
        # TODO makes sure this card is valid
        return card_to_play_index

    def learn(self):
        if self.memory.mem_cntr < self.batch_size:
            return # TODO this might be good place for file reading
        
        if self.learn_step_counter % self.replace == 0:
            # If replace many learning actions have been taken since the last time the
            # target network was updated, then update the target network
            # https://youtu.be/CoePrz751lg?t=1594
            self.q_next.set_weights(self.q_eval.get_weights())

        # the \ on the next line just lets python know that the line continues on the next line
        # TODO we might actually want to consier using the \ in other places in our code
        states, actions, rewards, states_, dones = \
                                            self.memory.sample_buffer(self.batch_size)
        # Pull in information about a game from the buffer

        # TODO Don't quite know what this is doing
        q_pred = self.q_eval(states)
        # This gets the value of the max future action
        q_next = tf.math.reduce_max(self.q_next(states_), axis=1, keepdims=True).numpy()
        # need to copy the prediction network because of the way keras handles calculating loss
        # https://youtu.be/CoePrz751lg?t=1698
        q_target = np.copy(q_pred)
        # NOTE: I don't like the naming here since there's a target network in use that's called next,
        # then we get this copied network that's called target. This seems confusing.

        #room for improvement here?
        for index, terminal in enumerate(dones):
            if terminal:
                # terminal indicates that we've reached the end of a game, and as such
                # the future reward must be 0
                q_next[index] = 0.0
            # https://youtu.be/CoePrz751lg?t=1819
            q_target[index, actions[index]] = rewards[index] + self.gamma*q_next[index]
        # TODO: Not really sure what this is doing
        self.q_eval.train_on_batch(states, q_target)
        # decrement the epsilon value, make plays less randomly as tranining progresses
        self.epsilon = self.epsilon - self.epsilon_dec if self.epsilon > \
                        self.epsilon_min else self.epsilon_min
        # Increment the counter of how many training runs have been done
        self.learn_step_counter += 1

#    def save_model(self):
#        self.q_eval.save(self.model_file)

#    def load_model(self):
#        self.q_eval = load_model(self.model_file)

# ^NOTE: This is the end of the transcribed sample code, I'm sure there's was we can modify it to suit our needs.
        
# Code spiking group file read
if __name__ == "__main__":
    training_data = glob2.glob("*.spzd") # creates a list of all files ending in .spzd

#    print(training_data)
    file_count = len(training_data)
    #random.shuffle(training_data)
    testing_data = []
    while len(training_data) > int(file_count*0.9): # randomize the list then move 10% of them to the testing data set
        testing_data.append(training_data.pop())
    with ExitStack() as stack: # setup an exitstack so multiple files can be safely opened at the same time.
        files = [stack.enter_context(open(fname, 'rb')) for fname in training_data] # open all the files in the training_data list
        file_data = pickle.load(files[0])
        for data in file_data:
            print(data["player_score_history"])
        # from the last file in the list, get the data from the last trick played, from that get the player_partner_prediction_history, then get the last element of that
