#"2020-03-31 15;36;43,063005_game_id_0.spzd"
import random
import tensorflow as tf
import glob2
import pickle
import random
from contextlib import ExitStack

# what are we computing loss against?
# seperate training from running
# different networks for different tasks? playing cards, predicting partners, making calls


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
