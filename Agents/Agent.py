from GameObjects import *
import tensorflow as tf
from abc import ABC, abstractmethod
class Agent(ABC): #currently unsure what other information an agent should have?

    _player_interface = None # single _ because the subclasses will want access to this as well
    _weighted_call_list = []
    _weighted_card_list = []

    def __init__(self, a_player):
        self._player_interface = a_player

    @abstractmethod
    def make_call(self, game_state):
        pass

    @abstractmethod
    def play_card(self, game_state):
        pass
