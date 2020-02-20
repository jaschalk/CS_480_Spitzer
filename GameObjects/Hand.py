from GameObjects import Card
from GameObjects import Trick
import numpy as np

class Hand:
    
    _cards_in_hand = []
    _valid_play_list = []
    _my_player = None

    def __init__(self, a_player):
        self._my_player = a_player #Don't know if this is needed?
        pass

    def accept(self, a_card):
        self._cards_in_hand[a_card._card_id] = 1

    def determine_valid_play_list(self):
        #This method should ask the card rules to use its validate method on a card, a player, and a round?
        #What does the validate method in the card rules return? T/F?
        for index in range(8):
            self._my_player._parent_game._card_rules.validate_card(self._cards_in_hand[index], self._my_player, self._my_player._round)

    def play_valid_card(self, a_trick):
        #This method should play a card from the valid card list to the trick.