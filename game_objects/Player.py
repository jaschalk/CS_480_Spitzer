from game_objects.Hand import Hand
import numpy as np
from agents import agent

class Player:
    
    _trick_points = 0
    _round_points = 0
    _total_score = 0
    _valid_call_list = [1, 0, 0, 0, 0, 1, 1, 1]
    _potential_partners_list = [0, 0, 0, 0] #initialized to all zeroes when created because we don't know the id of the player
    _hand = None
    _is_leading = False
    _player_id = None
    _parent_game = None
    _controlling_agent = None
    _cards_played = 0

    def __init__(self, a_game, player_id, an_agent): 
        #initializes the hand object and sets the potential partners list to correct values.
        self._player_id = player_id
        self._parent_game = a_game
        self._controlling_agent = an_agent
        self._potential_partners_list = [0, 0, 0, 0] 
        self._potential_partners_list[self._player_id] = 1
        for index in range(4):
            if index != self._player_id:
                self._potential_partners_list[index] = (1/3)
        self._hand = Hand(self)

    def get_player_id(self):
        return self._player_id
    
    def get_trick_points(self):
        return self._trick_points

    def set_trick_points(self, a_trick_points):
        self._trick_points = a_trick_points

    def get_total_score(self):
        return self._total_score

    def set_total_score(self, a_total_score):
        self._total_score = a_total_score

    def get_round_points(self):
        return self._round_points
    
    def set_round_points(self, a_round_points):
        self._round_points = a_round_points

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

    def get_cards_played(self):
        return self._cards_played

    def get_is_leading(self):
        return self._is_leading

    def accept(self, a_card):
        #This method should send the card to the hand when a player is dealt a card
        a_card.set_owning_player(self.get_player_id())
        self._hand.accept(a_card)

    def play_card_to(self, a_trick):
        #Player asks agent to pick a card to play. The value returned from the agent is used to ask the hand to play a card at the inex returned to the trick.
        card_to_play_index = self._controlling_agent.play_card(self, self._parent_game) #This is the index of the card to be played in the player's hand
        self._hand.play_card_at_index(a_trick, card_to_play_index)
    
    def validate_card(self, a_card):
        #Ask the game to run its validate card method on the card passed in. Return this information to the hand.
        return self._parent_game.validate_card(a_card, self)

    def determine_potential_partners(self):
        #Asks the parent game to use its validate partners method to modify the potential partners list based on the returned string.
        _result = ""
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
        #Player asks agent to make a call. The value returned from the agent is then used to update the round based on the index of the call made.
        index_of_call_made = self._controlling_agent.make_call(self)
        self._parent_game.update_call(self._player_id, index_of_call_made)

    def determine_valid_calls(self):
        #Asks the parent game to return the legal calls based on the information in the hand.
        self._valid_call_list = self._parent_game.validate_calls(self._hand)

    def does_play_continue(self):
        #If there are no more cards in the hand, play should not continue.
        if len(self._hand.get_cards_in_hand()) == 0:
            return False
        else:
            return True