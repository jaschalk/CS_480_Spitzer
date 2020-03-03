from agents.agent import Agent

class CustomAgent(Agent):

    def estimate_strength_of_hand(self, cards_in_hand_list):
        pass
    
    def make_call(self, cards_in_hand_list):
        
        pass

    def play_card(self, game_state):
        #game_state is expected to be a dict containing the trick history, trick point history, call matrix, current trick, and the current player
        pass