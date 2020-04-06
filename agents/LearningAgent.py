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
    def __init__(self, n_actions, fc1_dims, fc2_dims):
        super(DuelingDeepQNetwork, self).__init__()
        self.dense1 = keras.layers.Dense(fc1_dims, activation="relu")
        self.dense2 = keras.layers.Dense(fc2_dims, activation="relu")
        self.V = keras.layers.Dense(1, activation=None)
        self.A = keras.layers.Dense(n_actions, activation=None)

    def call(self, state):
        x = self.dense1(state)
        x = self.dense2(x)
        V = self.V(x)
        A = self.A(x)

        Q = (V + (A - tf.reduce_mean(A, axis=1, keepdims=True)))

        return Q

    def advantage(self, state):
        x = self.dense1(state)
        x = self.dense2(x)
        A = self.A(x)

        return A

class ReplayBuffer():
    def __init__(self, max_size, input_shape):
        self.mem_size = max_size
        self.mem_cntr = 0

        self.state_memory = np.zeros((self.mem_size, *input_shape),
                                        dtype=np.float32)
        self.new_state_memory = np.zeros((self.mem_size, *input_shape),
                                        dtype=np.float32)
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
        # TODO I think our file read might go here?
        max_mem = min(self.mem_cntr, self.mem_size)
        batch = np.random.choice(max_mem, batch_size, replace=False)

        states = self.state_memory[batch]
        new_states = self.new_state_memory[batch]
        actions = self.action_memory[batch]
        rewards = self.reward_memory[batch]
        dones = self.terminal_memory[batch]

        return states, actions, rewards, new_states, dones

class Agent():
    def __init__(self, lr, gamma, n_actions, epsilon, batch_size,
                    input_dims, epsilon_dec=1e-3, epsilon_min=1e-3,
                    mem_size=100000, fname='dueling_dqn.h5', fc1_dims=128, # TODO The dims need to be changed
                    fc2_dims=128, replace=500):
        self.action_space = [i for i in range(n_actions)]
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_dec = epsilon_dec
        self.epsilon_min = epsilon_min
        self.fname = fname
        self.replace = replace
        self.batch_size = batch_size
        self.learn_step_counter = 0
        self.memory = ReplayBuffer(mem_size, input_dims)
        self.q_eval = DuelingDeepQNetwork(n_actions, fc1_dims, fc2_dims)
        self.q_next = DuelingDeepQNetwork(n_actions, fc1_dims, fc2_dims)
        self.q_eval.compile(optimizer=Adam(learning_rate=lr), loss='mean_squared_error')
        # the next network isn't actually optimized here, this is just needed to make it work?
        self.q_next.compile(optimizer=Adam(learning_rate=lr), loss='mean_squared_error')

    def store_transition(self, state, action, reward, new_state, done):
        self.memory.store_transition(state, action, reward, new_state, done)

    def choose_action(self, observation):
        if np.random.random() < self.epsilon:
            action = np.random.choice(self.action_space)
        else:
            state = np.array([observation])
            actions = self.q_eval.advantage(state)
            action = tf.math.argmax(actions, axis=1).numpy()[0]

        return action

    def learn(self):
        if self.memory.mem_cntr < self.batch_size:
            return # TODO this might also be good place for file reading
        
        if self.learn_step_counter % self.replace == 0:
            self.q_next.set_weights(self.q_eval.get_weights())

        # the \ on the next line just lets python know that the line continues on the next line
        # TODO we might actually want to consier using the \ in other places in our code
        states, actions, rewards, states_, dones = \
                                            self.memory.sample_buffer(self.batch_size)

        q_pred = self.q_eval(states)
        q_next = tf.math.reduce_max(self.q_next(states_), axis=1, keepdims=True).numpy()
        q_target = np.copy(q_pred)
        #room for improvement here?
        for index, terminal in enumerate(dones):
            if terminal:
                q_next[index] = 0.0
            q_target[index, actions[index]] = rewards[index] + self.gamma*q_next[index]
        self.q_eval.train_on_batch(states, q_target)
        self.epsilon = self.epsilon - self.epsilon_dec if self.epsilon > \
                        self.epsilon_min else self.epsilon_min

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
            print(data["player_partners"])
        # from the last file in the list, get the data from the last trick played, from that get the player_partner_prediction_history, then get the last element of that
