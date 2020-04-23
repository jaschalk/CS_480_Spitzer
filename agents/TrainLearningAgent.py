from game_objects.Game import Game
from agents.LearningAgent import Agent
from agents.CustomAgent import CustomAgent
from agents.RandomAgent import RandomAgent
import random

if __name__ == "__main__":
    
    # Do we want to balance the occurence rates of the agents? Yes
    agent_types = [Agent, CustomAgent, RandomAgent]
    agent_weights = [.33, .66, 1]
    
    n_games = 25

    for i in range(n_games):
        list_of_agents = [Agent()]
        for i in range(3):
            rolled_weight = random.randrange(0,1)
            for index in range(len(agent_types)):
                if rolled_weight <= agent_weights[index]:
                    list_of_agents.append(agent_types[index]())
        random.shuffle(list_of_agents)
        active_game = Game(i, list_of_agents) #Initialization of a game
        active_game.play_game()