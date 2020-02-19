from GameObjects import *

class Game:

   _game_id = None
   _deck = None
   _round = None
   _players_list = [None, None, None, None]
   _card_rules = None
   _partner_rules = None
   _call_rules = None

   def __init__(self, a_game_id): #initializes the deck, round, players list, and all three sets of rules.
      self._game_id = a_game_id
      self._deck = Deck.Deck()
      self._round = Round.Round(self)
      for index in range(4):
        self._players_list[index] = Player.Player(index)
      self._card_rules = CardRuleTree.CardRuleTree(self)
      self._partner_rules = PartnerRuleTree.PartnerRuleTree(self)
      self._call_rules = CallRules.CallRules(self)

   def _begin_round(): #tells the round to use its begin play method
      self._round._begin_play()