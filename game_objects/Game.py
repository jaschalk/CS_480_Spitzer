from game_objects import *

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
        self._players_list[index] = Player.Player(self, index) #need to pass in an agent?
      self._card_rules = CardRuleTree.CardRuleTree()
      self._partner_rules = PartnerRuleTree.PartnerRuleTree(self)
      self._call_rules = CallRules.CallRules(self)

   def get_round(self):
      return self._round

   def begin_round():
      self._round._begin_play()

   def validate_card(self, a_card, a_player):
      #Accesses the card rules and returns whether or not the card passed in is valid to the player.
      return self._card_rules.validate_card(a_card, a_player, self._round)

   def validate_partners(self, asking_player, target_player_index):
      #Accesses the partner rules and returns whether or not two players are partners to the player.
      return self._partner_rules.validate_partners(asking_player, self._players_list[target_player_index], self._round)

   def validate_calls(self, a_hand):
      #Accesses the call rules and returns the list of valid calls to the player.
      return self._call_rules.validate_calls(a_hand.get_binary_representation())