from game_objects.Game import Game
from agents.LearningAgent import Agent
from agents.CustomAgent import CustomAgent
from agents.RandomAgent import RandomAgent
import time
import random

if __name__ == "__main__":
    random.seed(time.localtime())
    # Do we want to balance the occurence rates of the agents? Yes
    agent_types = [Agent, CustomAgent, RandomAgent]
    agent_weights = [1.0/9.0, 5.0/9.0, 1]
    
    n_games = 5
    start = time.perf_counter()
    for i in range(n_games):
        list_of_agents = []
        list_of_agents.append(Agent())
        for i in range(3):
            rolled_weight = random.random()
            for index in range(len(agent_types)):
                if rolled_weight <= agent_weights[index]:
                    list_of_agents.append(agent_types[index]())
                    break
        random.shuffle(list_of_agents)
#        print(list_of_agents)
        active_game = Game(i, list_of_agents) #Initialization of a game
        active_game.play_game()
    end = time.perf_counter()
    print(f"Ran {n_games} in {(end-start)} seconds.")
