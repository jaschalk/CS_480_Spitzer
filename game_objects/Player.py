from game_objects import *
from agents import agent

class Player:
    
    _trick_score = 0
    _round_score = 0
    _total_score = 0
    _trick = None #might want to double check if we need this.
    _valid_call_list = [1, 0, 0, 0, 1, 1, 1, 1]
    _potential_partners_list = [0, 0, 0, 0] #initialized to all zeroes when created because we don't know the id of the player
    _hand = None
    _is_leading = False
    _took_first_trick = False
    _player_id = None
    _parent_game = None
    _controlling_agent = None

    def __init__(self, a_game, player_id, an_agent): 
        #initializes the hand object and sets the potential partners list to correct values.
        self._player_id = player_id
        self._parent_game = a_game
        self._controlling_agent = an_agent 
        self._trick = Trick.Trick(a_game.get_round(), self) 
        self._potential_partners_list[self._player_id] = 1
        for index in range(4):
            if index != self._player_id:
                self._potential_partners_list[index] = (1/3)
        self._hand = Hand.Hand(self)

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

    def ask_for_card_choice(self):
        self._controlling_agent.play_card(self, self._parent_game) #need to better define what goes into the game state.
    
    def relay_card_choice(self, a_card_index): 
        #Ask the hand to play a card specified by the agent.
        self._hand.play_card_at_index(self._trick, a_card_index) #might want to consider relaying to the round instead of the trick.

    def validate_card(self, a_card):
        #Ask the game to run its validate card method on the card passed in. Return this information to the hand.
        return self._parent_game.validate_card(a_card, self)

    def determine_potential_partners(self):
        #Asks the parent game to use its validate partners method to modify the potential partners list based on the returned string.
        for index in range(4):
            if index != self._player_id:
                _result = self._parent_game.validate_partners(self, index)
            if _result == "target is my partner":
                self._potential_partners_list[index] = 1
            elif _result == "target is not my partner":
                self._potential_partners_list[index] = 0
                for i in range(4):
                    if i != self._player_id or index:
                      self._potential_partners_list[i] = 1/2 #This number might need to be modified later.

    def ask_for_call(self):
        self._controlling_agent.make_call(self)
    
    def relay_call_choice(self, a_call_index):
        #the player has to relay the call being made to the round -- might want to take another look at this.
        self._round.update_call(self._player_id, a_call_index)

    def determine_valid_calls(self):
        #Asks the parent game to return the legal calls based on the information in the hand.
        self._valid_call_list = self._parent_game.validate_calls(self._hand)

    def does_play_continue(self):
        #If there are no more cards in the hand, play should not continue.
        if self._hand.get_cards_in_hand().size() == 0:
            return False
        else:
            return True