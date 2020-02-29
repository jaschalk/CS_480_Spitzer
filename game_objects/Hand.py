from game_objects import Card
from game_objects import Trick
import numpy as np

class Hand:
    
    _cards_in_hand = []
    _binary_representation = 0
    _valid_play_list = []
    _my_player = None

    def __init__(self, a_player):
        self._my_player = a_player
        self._cards_in_hand = []
        self._valid_play_list = []
        self._binary_representation = 0

    def get_cards_in_hand(self):
        return self._cards_in_hand

    def get_binary_representation(self):
        return self._binary_representation

    def get_valid_play_list(self):  #Setting the valid play list is only done through the determine valid play list method.
        return self._valid_play_list

    def get_my_player(self):
        return self._my_player

    def accept(self, a_card):
        self._cards_in_hand.append(a_card)
        card_id = a_card.get_card_id()
        self._binary_representation += 1<<card_id

    def determine_valid_play_list(self):
        #Asks the player to use its validate card method on every card in the hand and set the return value to the valid play list.
        #self._valid_play_list = list(map(self._my_player.validate_card, self._cards_in_hand))
        self._valid_play_list.clear()
        for index in range(len(self._cards_in_hand)):
            print(self._cards_in_hand[index])
            self._valid_play_list.append(self._my_player.validate_card(self._cards_in_hand[index]))

    def play_card_at_index(self, a_trick, a_card_index):
        #Tell the trick to accept the card specified by the agent.
        self._binary_representation -= 1<<(self._cards_in_hand[a_card_index].get_card_id())
        a_trick.accept(self._cards_in_hand.pop(a_card_index))

    def determine_valid_calls(self):
        #Ask the player to determine what valid calls it can make based on the hand.
        self._my_player.determine_valid_calls()