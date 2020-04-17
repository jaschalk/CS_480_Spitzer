from game_objects import Card
from game_objects import Trick
import numpy as np

class Hand:

    def __init__(self, a_player):
        self._my_player = a_player
        self.set_initial_values()

    def set_initial_values(self):
        self._cards_in_hand = []
        self._valid_play_list = [1, 1, 1, 1, 1, 1, 1, 1]
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
        self._valid_play_list = [0 for i in range(8)]
        for index in range(len(self._cards_in_hand)):
            self._valid_play_list[index] = self._my_player.validate_card(self._cards_in_hand[index])
#        print(f"The valid play list has been set to {self._valid_play_list}")

    def play_card_at_index(self, a_trick, a_card_index):
        #Tell the trick to accept the card specified by the agent.
        print(f"Card index to be played: {a_card_index}")
        print(f"Length of cards in hand list: {len(self._cards_in_hand)}")
        card_to_be_played_id = self._cards_in_hand[a_card_index].get_card_id()

        # TODO This check is causing tests to fail, figure out why!
        # NOTE: the agents seem to be having an issue when the is only 1 valid card to play
        # Random tries to play the first card
        # Custom tries to play the last
        # TODO: Sometimes there's also nonsensical valid play lists when the trick is empty
        # I think this is a seperate problem
#        print(f"With valid play list of: {self._valid_play_list}")
#        print(f"Cards in hand: {self._cards_in_hand}")
        if self._valid_play_list[a_card_index] == False:
            print()
            print(f"Valid play list is: {[(card.get_card_id(), playable) for card, playable in zip(self._cards_in_hand,self._valid_play_list)]}")
            print(f"Can't play {self._cards_in_hand[a_card_index].get_card_id()} at position {a_card_index} to trick with cards {[card.get_card_id() for card in a_trick.get_played_cards_list() if card is not None]}")
            print(f"Agent type is: {self._my_player.get_controlling_agent()}")
            print()
            raise Exception("Attempting to play a card that can't be played")
        self._my_player._cards_played += 1<<(card_to_be_played_id)
        self._binary_representation -= 1<<(card_to_be_played_id)
        a_trick.accept(self._cards_in_hand.pop(a_card_index))

    def determine_valid_calls(self):
        #Ask the player to determine what valid calls it can make based on the hand.
        self._my_player.determine_valid_calls()