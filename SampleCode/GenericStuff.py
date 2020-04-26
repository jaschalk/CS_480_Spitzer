import glob2
import pickle
import copy
import sys
import random
import time
import uuid
import re
from contextlib import ExitStack
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import numpy as np

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

def graph_results():
    matches = []
    winners = []
    game_count = 0.0
    total_points_taken = [0, 0, 0]
    total_tricks_played = 0.0
    agent_win_counts = [0.0, 0.0, 0.0]
    ml_agent_player_numbers = []
    agent_type_point_taken_lists = [0, 0, 0]
    custom_agent_player_numbers = []
    random_agent_player_numbers = []
    random_agent_graph_data = [[],[]]
    custom_agent_graph_data = [[],[]]
    learning_agent_graph_data = [[],[]]
    learning_average_trick_points_graph_data = [[],[]]
    custom_average_trick_points_graph_data = [[],[]]
    random_average_trick_points_graph_data = [[],[]]
    random_x = np.linspace(0, 1, 100)
    print(random_x)

    with open('game_winner_info.txt', 'r') as input:
        line = input.read()
        file_name_matcher = re.compile(r'file: (.+\.spzd)\n\w+ (\d).+\.(\w+)\..+\n.+\.(\w+)\..+k (\d+)\n.+\.(\w+)\..+k (\d+)\n.+\.(\w+)\..+k (\d+)\n.+\.(\w+)\..+k (\d+)\n')
        test = file_name_matcher.finditer(line)
        for i in test:
            game_count += 1.0
            #print(f"File name is: {i.group(1)}")
            associated_file_name = i.group(1)
            #print(f"Winning player is: {i.group(2)}")
            if i.group(3) == "RandomAgent":
                agent_win_counts[0] += 1.0
            elif i.group(3) == "CustomAgent":
                agent_win_counts[1] += 1.0
            elif i.group(3) == "LearningAgent":
                agent_win_counts[2] += 1.0
            # This is finding the win ratios of the random agent, custom agent, and learning agent across a set of games
#            print(f"{agent_win_counts[0]/game_count}  {agent_win_counts[1]/game_count}  {agent_win_counts[2]/game_count}")
            random_agent_win_ratio = agent_win_counts[0]/game_count
            random_agent_graph_data[0].append(game_count)
            random_agent_graph_data[1].append(random_agent_win_ratio)
            custom_agent_win_ratio = agent_win_counts[1]/game_count
            custom_agent_graph_data[0].append(game_count)
            custom_agent_graph_data[1].append(custom_agent_win_ratio)
            learning_agent_win_ratio = agent_win_counts[2]/game_count
            learning_agent_graph_data[0].append(game_count)
            learning_agent_graph_data[1].append(learning_agent_win_ratio)

            for index in range(4, 11, 2):
                if i.group(index) == "LearningAgent":
                    ml_agent_player_numbers.append((index-4)//2)
                if i.group(index) == "CustomAgent":
                    custom_agent_player_numbers.append((index-4)//2)
                if i.group(index) == "RandomAgent":
                    random_agent_player_numbers.append((index-4)//2)
            agent_numbers_lists = [ml_agent_player_numbers, custom_agent_player_numbers, random_agent_player_numbers]

            agent_average_trick_points_graph_data = [learning_average_trick_points_graph_data, custom_average_trick_points_graph_data, random_average_trick_points_graph_data]
            with open(associated_file_name, 'rb') as data_file:
                file_data = pickle.load(data_file)
                trick_point_history = file_data[-1]["trick_point_history"]
                for trick_index in range(8):
                    total_tricks_played += 1.0
                    for player_id in range(4):
                        for agent_type_index in range(3):
                            if player_id in agent_numbers_lists[agent_type_index]:
                                agent_average_trick_points_graph_data[agent_type_index][0].append(total_tricks_played)
                                total_points_taken[player_id] += trick_point_history[player_id]
                                agent_type_point_taken_lists[agent_type_index] += total_points_taken[player_id]
                                agent_average_trick_points_graph_data[agent_type_index][1].append(agent_type_point_taken_lists[agent_type_index]/total_tricks_played)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=learning_agent_graph_data[0], y=learning_agent_graph_data[1], name='Learning Agent'))
    fig.add_trace(go.Scatter(x=custom_agent_graph_data[0], y=custom_agent_graph_data[1], name='Custom Agent'))
    fig.add_trace(go.Scatter(x=random_agent_graph_data[0], y=random_agent_graph_data[1], name='Random Agent'))
    fig.show()

    trick_average_graph = go.Figure()
    for i in range(3):
        trick_average_graph.add_trace(go.Scatter(x=agent_average_trick_points_graph_data[i][0], y=agent_average_trick_points_graph_data[i][1], name='Agent Points/Trick'))
    trick_average_graph.show()

if __name__ == "__main__":
    graph_results()
#    test = [0.3333333333, 1]
#    totals = [0.0, 0.0]
#    count = 5000
#    for i in range(count):
#        totals[0] += 1
#        for x in range(3):
#            r = random.random()
#            for k in range(2):
#                if r < test[k]:
#                    totals[k] += 1
#                    break

#    print(totals[0]/sum(totals), totals[1]/sum(totals))
