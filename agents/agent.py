from game_objects import *
import tensorflow as tf
from abc import ABC, abstractmethod
class Agent(ABC): #currently unsure what other information an agent should have?

    _weighted_call_list = []
    _weighted_card_list = []

    def __init__(self, a_player):
        self._player_interface = a_player

    @abstractmethod
    def make_call(self, game_state): #use the return values to get information back to the player object within the system.
        pass

    @abstractmethod
    def play_card(self, game_state):
        pass