from game_objects.Deck import Deck
from game_objects.Round import Round
from game_objects.Player import Player
from game_objects.CardRuleTree import CardRuleTree
from game_objects.CallRules import CallRules
from game_objects.PartnerRuleTree import PartnerRuleTree
from random import randint
from enums import CardIds

class Game:

   _scoring_table = [["impossible", -9, -6, 3, 6, 9],
                     ["impossible", -9, -6, 9, 12, 15],
                     [-15, -12, -9, 18, 27, 36],
                     [-42, -36, -24, -18, 36, 39],
                     [-42, -42, -39, -33, -27, 42]]

   def __init__(self, a_game_id, list_of_agents): #initializes the deck, round, players list, and all three sets of rules.
      self._game_id = a_game_id
      self._players_list = [None, None, None, None]
      self._deck = Deck()
      for index in range(4):
         self._players_list[index] = Player(self, index, list_of_agents[index])
      self._leading_player = self._players_list[randint(0,3)]
      self._round = Round(self) #Had to move this down to after the players are setup, since the round pulls that info from the game
      self._card_rules = CardRuleTree()
      self._partner_rules = PartnerRuleTree()
      self._call_rules = CallRules()
      self._score_list = [0, 0, 0, 0]

   def get_game_id(self):
      return self._game_id

   def get_round(self):
      return self._round

   def get_trick(self):
      return self._round.get_current_trick()

   def get_deck(self):
      return self._deck

   def play_game(self):
      self.clean_up_round_file_data()
      while self.which_player_wins() == -1:
         self._round.set_initial_values()
         self.begin_round()
      self._round.push_data_to_file()

   def begin_round(self):
      self._deck.populate_deck()
      for player in self._players_list:
         self._deck.deal_cards_to(player)
         self._round.update_player_cards_in_hand_history_for_player(player)
      self._round.begin_play()

   def get_players_list(self):
      return self._players_list

   def get_call_rules(self):
      return self._call_rules

   def get_card_rules(self):
      return self._card_rules

   def get_partner_rules(self):
      return self._partner_rules

   def get_leading_player(self):
      return self._leading_player

   def get_score_list(self):
      return self._score_list

   def clean_up_round_file_data(self):
      self._round.clear_file_out_history()

   def get_game_state_for_player(self, a_player_id):
      return self._round.get_game_state_for_play_card(a_player_id)

   def which_player_wins(self):
      #Check scores of all players and return the index of the winning player. If there is no winner, it should return -1.
      num_of_winners = 0
      winning_index = -1
      max_score = max(self._score_list)
      for index in range(4):
         if self.get_players_list()[index].get_total_score() >= 42 and self.get_players_list()[index].get_total_score() >= max_score:
            num_of_winners += 1
            winning_index = index
      if num_of_winners != 1:
         return -1
      else:
         return winning_index

   def validate_card(self, a_card, a_player):
      #Accesses the card rules and returns whether or not the card passed in is valid to the player.
      return self._card_rules.validate_card(a_card, a_player, self._round)

   def validate_partners(self, asking_player, target_player_index):
      #Accesses the partner rules and returns whether or not two players are partners to the player.
      return self._partner_rules.validate_partners(asking_player, self._players_list[target_player_index], self._round)

   def validate_calls(self, a_hand):
      #Accesses the call rules and returns the list of valid calls to the player.
      return self._call_rules.validate_calls(a_hand.get_binary_representation())

   def update_call(self, player_id, index_of_call_index):
      self._round.update_call(player_id, index_of_call_index)

   def update_scores(self):
      #Can this method be shortened at all?
      call_index = 0
      calling_player_id = -1
      calling_team = []
      calling_team_round_points = 0
      point_value_index = -1
      played_queen_of_clubs = -1
      played_queen_of_spades = -1
      def find_call_made():
         nonlocal calling_player_id
         nonlocal call_index
         for player_index in range(4):
            for call_made in range(1,8):
               if(self._round.get_call_matrix()[player_index][call_made] == 1):
                  call_index = call_made
                  if call_index < 5:
                     call_index = 0
                  else:
                     call_index -= 3
                  calling_player_id = player_index
                  return call_made
         return 0
      call_made = find_call_made()

      # split off into a helper method?
      if(call_made == 0):
         for player_index in range(4):
            for trick_index in range(8):
               if(self._round.get_trick_history()[player_index][trick_index][CardIds.queen_clubs.value] == 1): #If this player played the QC in any trick
                  played_queen_of_clubs = player_index
               elif(self._round.get_trick_history()[player_index][trick_index][CardIds.queen_spades.value] == 1):#If this player played the QS in any trick
                  played_queen_of_spades = player_index
         if(played_queen_of_clubs == played_queen_of_spades):
            calling_team = [played_queen_of_clubs]
            call_index = 1
         else:
            calling_team = [played_queen_of_clubs, played_queen_of_spades]
      else:
         calling_ppl = self._players_list[calling_player_id].get_potential_partners_list()
         for player_id in range(4):
            if(calling_ppl[player_id] == 1):
               calling_team.append(player_id)

      for i in range(4):
         if i in calling_team:
            calling_team_round_points += self._players_list[i].get_round_points()

      # split off into a helper method?
      noncalling_team = set(range(4)).difference(set(calling_team))
      if set(self._round.get_trick_winners_list()).isdisjoint(set(calling_team)):
         point_value_index = 0
      elif set(self._round.get_trick_winners_list()).isdisjoint(noncalling_team):
         point_value_index = 5
      else:
         if(calling_team_round_points <= 30):
            point_value_index = 1
         elif(calling_team_round_points <= 60):
            point_value_index = 2
         elif(calling_team_round_points <= 89):
            point_value_index = 3
         elif(calling_team_round_points <= 120):
            point_value_index = 4
         else:
            point_value_index = -1
            raise Exception("Calling team round points didn't resolve to an index. " + str(calling_team_round_points) + "\r\n" + str([player.get_round_points() for player in self._players_list]))

      for player_index in range(4):
         value_to_add = self._scoring_table[call_index][point_value_index]
         if type(value_to_add) == type("string"):
            print("In unreachable state")
            raise Exception("Entered an unreachable state in the scoring table.")
         if player_index in calling_team:
            if(value_to_add > 0):
               self._players_list[player_index].update_total_score(value_to_add)
               self._score_list[player_index] = self._players_list[player_index].get_total_score()

         else:
            if(value_to_add < 0):
               self._players_list[player_index].update_total_score(abs(value_to_add))
               self._score_list[player_index] = self._players_list[player_index].get_total_score()

      self._round.update_player_score_history([self._players_list[player_index].get_total_score() for player_index in range(4)])