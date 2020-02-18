from GameObjects import *

class Game:

   _game_id = None
   _deck = None
   _round = None
   _players_list = [None, None, None, None]
   _card_rules = None
   _partner_rules = None
   _call_rules = None

   def __init__(self, a_game_id): #Should the calls to initialize everything happen in the constructor?
      self._game_id = a_game_id
      for index in range(4):
        self._players_list[index] = Player()