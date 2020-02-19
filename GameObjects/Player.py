from GameObjects import *

class Player:
    
    _trick_score = 0
    _round_score = 0
    _total_score = 0
    _trick = None
    _valid_call_list = [1, 0, 0, 0, 1, 1, 1, 1]
    _potential_partners_list = [0, 0, 0, 0] #initialized to all zeroes when created because we don't know the id of the player
    _hand = None
    _is_leading = False #Should we use gets and sets for isLeading and tookFirstTrick?
    _took_first_trick = False

    def __init__(self, a_game, player_id): #initializes the hand object and sets the potential partners list to correct values.
        self._trick = Trick()
        self._potential_partners_list[player_id] = 1
        for index in range(4):
            if index != player_id:
                self._potential_partners_list[index] = (1/3)
        self._hand = Hand()

    def get_trick_score(self):
        return self._trick_score

    def set_trick_score(self, a_trick_score):
        self._trick_score = a_trick_score

    def get_total_score(self):
        return self._total_score

    def set_total_score(self, a_total_score):
        self._total_score = a_total_score

    def get_round_score(self):
        return self._round_score
    
    def set_round_score(self, a_round_score):
        self._round_score = a_round_score

    def get_valid_call_list(self):
        return self._valid_call_list

    def set_valid_call_list(self, a_valid_call_list):
        self._valid_call_list = a_valid_call_list

    def get_potential_players_list(self):
        return self._potential_partners_list
    
    def set_potential_partners_list(self, a_potential_partners_list):
        self._potential_partners_list = a_potential_partners_list

    def get_hand(self):
        return self._hand

    def set_hand(self, a_hand):
        self._hand = a_hand

    def play_card(self): #Ask the hand to play a valid card.
        self._hand.play_valid_card(self._trick) #Might need to re-think this behavior to include the agent

    def determine_potential_partners(self):
        #This method should use the current potential partners list and the partner rules
        #to change the potential partners list after new information has been gathered.

    def determine_valid_calls(self):
        #This method should use the current valid call list and call rules to change
        #the valid calls list based on the cards in the players hand.