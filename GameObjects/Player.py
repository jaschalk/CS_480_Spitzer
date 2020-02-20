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
    _player_id = None
    _parent_game = None

    def __init__(self, a_game, player_id): #initializes the hand object and sets the potential partners list to correct values.
        self._player_id = player_id
        self._parent_game = a_game
        self._trick = Trick()
        self._potential_partners_list[self.player_id] = 1
        for index in range(4):
            if index != self.player_id:
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

    def get_potential_partners_list(self):
        return self._potential_partners_list
    
    def set_potential_partners_list(self, a_potential_partners_list):
        self._potential_partners_list = a_potential_partners_list

    def get_hand(self):
        return self._hand

    def set_hand(self, a_hand):
        self._hand = a_hand

    def accept(self, a_card):
        #This method should send the card to the hand when a player is dealt a card
        self._hand.accept(a_card)

    def play_card(self): #Ask the hand to play a valid card.
        self._hand.play_valid_card(self._trick) #Might need to re-think this behavior to include the agent

    def determine_potential_partners(self):
        #This method should ask the partner rules to run its validate method on two players
        #and set the potential partners list according to the string returned from that method.
        #I don't think I'm doing this right...
        #What about going from 1/3 to 1/2??
        for index in range(4):
            if index != self._player_id:
                _result = self._parent_game._partner_rules.validate_partners(self, self._parent_game._players_list[index], self._parent_game._round)
            if _result = "target is my partner":
                self._potential_partners_list[index] = 1
            elif _result = "target is not my partner":
                self._potential_partners_list[index] = 0
            else:
                #don't modify anything?

    def determine_valid_calls(self):
        #This method should ask the call rules to run its validate method on the current
        #call list (and the cards in the players hand?) and re-set the call list to the 
        #value returned from that method.