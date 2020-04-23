import glob2
import pickle
import copy
import sys
import random
import time
from contextlib import ExitStack

if False:
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

if __name__ == "__main__":
    random.seed(time.localtime())
    weights = [1.0/9.0, 5.0/9.0, 1]
#    values = ['a', 'b', 'c']
    totals = [0, 0, 0]
    count = 2000
    for i in range(count):
        totals[0] += 1
        for i in range(3):
            rolled_weight = random.random()
            for index in range(len(totals)):
                if rolled_weight <= weights[index]:
                    totals[index] += 1
                    break
    ratios = [value/(sum(totals)) for value in totals]
    print(totals)
    print(ratios)