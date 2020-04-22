from game_objects.Game import Game
from agents.LearningAgent import Agent
from agents.CustomAgent import CustomAgent

if __name__ == "__main__":
    agent = Agent()
    list_of_agents = [agent, CustomAgent(), CustomAgent(), CustomAgent()]
    active_game = Game(0, list_of_agents) #Initialization of a game
    n_games = 500
    
    scores, eps_history = [], []

    for i in range(n_games):
        done = False #Game's has_ended method --Might not have a way to store this yet.
        score = 0
        observation = active_game.get_game_state() #Our get_game_state_for...?
        print(type(observation))
        while active_game.which_player_wins() == -1: #While the game hasn't ended...
            action = agent.choose_action(observation) #Here there is a disconnect between choosing an action and stepping the env. In ours, there isn't one yet.
            observation_, reward, done, info = active_game.get_player.handle_action(action) #Currently shooting for the end of every trick.
            score += reward
            agent.store_transition(observation, action, reward, observation_, done) #This stores the result observation from the action. We aren't doing this yet either.
            observation = observation_ #The game's observation is reset to the observation after a specific action has been made and the env has been stepped.
            agent.learn() #Updates the weights of the network?