from GameObjects import *
import tensorflow as tf
class Agent: #currently unsure what other information an agent should have?

    _player_interface = None # single _ because the subclasses will want access to this as well

    def __init__(self, a_player):
        self._player_interface = a_player
