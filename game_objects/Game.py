from game_objects.Deck import Deck
from game_objects.Round import Round
from game_objects.Player import Player
from game_objects.CardRuleTree import CardRuleTree
from game_objects.CallRules import CallRules
from game_objects.PartnerRuleTree import PartnerRuleTree

class Game:

   _game_id = None
   _deck = None
   _round = None
   _players_list = [None, None, None, None]
   _card_rules = None
   _partner_rules = None
   _call_rules = None

   def __init__(self, a_game_id, list_of_agents): #initializes the deck, round, players list, and all three sets of rules.
      self._game_id = a_game_id
      self._deck = Deck()
      self._round = Round(self)
      for index in range(4):
        self._players_list[index] = Player(self, index, list_of_agents[index])
      self._card_rules = CardRuleTree()
      self._partner_rules = PartnerRuleTree()
      self._call_rules = CallRules()

   def get_round(self):
      return self._round

   def get_deck(self):
      return self._deck

   def begin_round(self):
      for player in self._players_list:
         self._deck.deal_cards_to(player)
      self._round.begin_play()

   def get_players_list(self):
      return self._players_list

   def get_call_rules(self):
      return self._call_rules

   def get_card_rules(self):
      return self._card_rules

   def get_partner_rules(self):
      return self._partner_rules

   def validate_card(self, a_card, a_player):
      print("In Game: ")
      print(a_card)
      print("Games Round:")
      print(self._round)
      #Accesses the card rules and returns whether or not the card passed in is valid to the player.
      return self._card_rules.validate_card(a_card, a_player, self._round)

   def validate_partners(self, asking_player, target_player_index):
      #Accesses the partner rules and returns whether or not two players are partners to the player.
      return self._partner_rules.validate_partners(asking_player, self._players_list[target_player_index], self._round)

   def validate_calls(self, a_hand):
      #Accesses the call rules and returns the list of valid calls to the player.
      return self._call_rules.validate_calls(a_hand.get_binary_representation())

   def update_call(self, player_id, index_of_call_made):
      self._round.update_call(player_id, index_of_call_made)