from game_objects.Game import Game
from agents.LearningAgent import Agent
from agents.CustomAgent import CustomAgent
from agents.RandomAgent import RandomAgent
import time
import random

def run_training_batch(n_games):
    random.seed(time.localtime())
    # Do we want to balance the occurence rates of the agents? Yes
    agent = Agent()
    agent_types = [agent, CustomAgent(), RandomAgent()]
    agent_weights = [1/9, 5.0/9.0, 1]
    
    start = time.perf_counter()
    
    for i in range(n_games):
        try:
            list_of_agents = []
            list_of_agents.append(agent)
            for i in range(3):
                rolled_weight = random.random()
                for index in range(len(agent_types)):
                    if rolled_weight <= agent_weights[index]:
                        list_of_agents.append(agent_types[index])
                        break
            random.shuffle(list_of_agents)
    #        print(list_of_agents)
            active_game = Game(i, list_of_agents) #Initialization of a game
            active_game.play_game()
        except Exception as err:
            print(f"well that didn't work... {err}")
    end = time.perf_counter()
    print(f"Ran {n_games} in {(end-start)} seconds.")
    return True

if __name__ == "__main__":
    while True:
        batch_result = run_training_batch(250)
        print("-------------Finished Batch-------------")
    