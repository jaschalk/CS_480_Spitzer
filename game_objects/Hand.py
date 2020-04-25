from game_objects import Card
from game_objects import Trick
import numpy as np

class Hand:

    def __init__(self, a_player):
        self._my_player = a_player
        self._starting_cards = [0 for i in range(32)]
        self.set_initial_values()

    def set_initial_values(self):
        self._cards_in_hand = []
        self._valid_play_list = [True for i in range(8)]
        self._binary_representation = 0

    def get_starting_cards(self):
        return self._starting_cards

    def get_cards_in_hand(self):
        return self._cards_in_hand

    def get_binary_representation(self):
        return self._binary_representation

    def get_valid_play_list(self):  #Setting the valid play list is only done through the determine valid play list method.
        return self._valid_play_list

    def initialze_valid_play_list(self):
        self._valid_play_list = [False for i in range(8)]
        for i in range(len(self._cards_in_hand)):
            self._valid_play_list[i] = True

    def get_my_player(self):
        return self._my_player

    def accept(self, a_card):
        self._cards_in_hand.append(a_card)
        card_id = a_card.get_card_id()
        self._starting_cards[card_id] = 1
        self._binary_representation += 1<<card_id

    def determine_valid_play_list(self):
        #Asks the player to use its validate card method on every card in the hand and set the return value to the valid play list.
        self._valid_play_list = [0 for i in range(8)]
        for index in range(len(self._cards_in_hand)):
            self._valid_play_list[index] = self._my_player.validate_card(self._cards_in_hand[index])

    def play_card_at_index(self, a_trick, a_card_index):
        #Tell the trick to accept the card specified by the agent.
        card_to_be_played_id = self._cards_in_hand[a_card_index].get_card_id()
        if self._valid_play_list[a_card_index] == False:
            card_list = [card.get_card_id() for card in self._cards_in_hand]
            trick_cards = [None, None, None, None]
            for index in range(4):
                if a_trick.get_played_cards_list()[index] != None:
                    trick_cards[index] = a_trick.get_played_cards_list()[index].get_card_id()
            display = f"\r\nAgent {self._my_player.get_controlling_agent()} is attempting to play a card that can't be played \r\n Cards in hand: {card_list} \r\n Valid Playlist: {self._valid_play_list} \r\n Playing: {a_card_index} \r\n To: {trick_cards}"
            raise Exception(display)
        self._my_player._cards_played += 1<<(card_to_be_played_id)
        self._binary_representation -= 1<<(card_to_be_played_id)
        a_trick.accept(self._cards_in_hand.pop(a_card_index))

    def determine_valid_calls(self):
        #Ask the player to determine what valid calls it can make based on the hand.
        self._my_player.determine_valid_calls()