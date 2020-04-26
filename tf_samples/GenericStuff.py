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
            # Get the player number of the learning agent:
            ml_agent_player_number = -1
            custom_agent_player_number = -1
            random_agent_player_number = -1
            for index in range(4, 11, 2):
                if i.group(index) == "LearningAgent":
                    ml_agent_player_number = (index-4)//2
                if i.group(index) == "CustomAgent":
                    custom_agent_player_number = (index-4)//2
                if i.group(index) == "RandomAgent":
                    random_agent_player_number = (index-4)//2

#            print(f"Agent id: {ml_agent_player_number}")
            with open(associated_file_name, 'rb') as data_file:
                file_data = pickle.load(data_file)
                total_tricks_played += 1.0
                trick_point_history = file_data[-1]["trick_point_history"]
                for trick_points in trick_point_history[ml_agent_player_number]:
                    total_points_taken[0] += trick_points
                    learning_average_trick_points_graph_data[0].append(total_tricks_played)
                    learning_average_trick_points_graph_data[1].append(total_points_taken[0]/total_tricks_played)
                for trick_points in trick_point_history[custom_agent_player_number]:
                    total_points_taken[1] += trick_points
                    custom_average_trick_points_graph_data[0].append(total_tricks_played)
                    custom_average_trick_points_graph_data[1].append(total_points_taken[1]/total_tricks_played)
                for trick_points in trick_point_history[random_agent_player_number]:
                    total_points_taken[2] += trick_points
                    random_average_trick_points_graph_data[0].append(total_tricks_played)
                    random_average_trick_points_graph_data[1].append(total_points_taken[2]/total_tricks_played)
#            print(f"average points/trick: {total_points_taken/total_tricks_played}")
            #print(f"Winning agent is: {i.group(3)}")
            #print(f"Player 0's agent: {i.group(4)}")
            #print(f"Scored: {i.group(5)}")
            #print(f"Player 1's agent: {i.group(6)}")
            #print(f"Scored: {i.group(7)}")
            #print(f"Player 2's agent: {i.group(8)}")
            #print(f"Scored: {i.group(9)}")
            #print(f"Player 3's agent: {i.group(10)}")
            #print(f"Scored: {i.group(11)}")
#    print(graph_data)
#    print(random_agent_graph_data[0])
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=learning_agent_graph_data[0], y=learning_agent_graph_data[1], name='Learning Agent'))
    fig.add_trace(go.Scatter(x=custom_agent_graph_data[0], y=custom_agent_graph_data[1], name='Custom Agent'))
    fig.add_trace(go.Scatter(x=random_agent_graph_data[0], y=random_agent_graph_data[1], name='Random Agent'))
    fig.show()
    trick_average_graph = go.Figure()
    trick_average_graph.add_trace(go.Scatter(x=learning_average_trick_points_graph_data[0], y=learning_average_trick_points_graph_data[1], name='Learning Agent Points/Trick'))
    trick_average_graph.add_trace(go.Scatter(x=custom_average_trick_points_graph_data[0], y=custom_average_trick_points_graph_data[1], name='Custom Agent Points/Trick'))
    trick_average_graph.add_trace(go.Scatter(x=random_average_trick_points_graph_data[0], y=random_average_trick_points_graph_data[1], name='Random Agent Points/Trick'))
    trick_average_graph.show()
#        file_name_matcher.findall()
#        for file_name in file_name_matcher.findall(line):
#            matches.append(file_name)
#    for match in matches:
#        with open(match, 'rb') as input:
#            file_data = pickle.load(input) # file_data should now be a list of dictionaries
#            print(file_data[-1]["trick_point_history"])

if __name__ == "__main__":
    graph_results()
