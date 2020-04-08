import pickle
import numpy as np
import copy
import os
import datetime
from enums import *
from game_objects.Trick import Trick

class Round:

    def __init__(self, a_game):
        self._parent_game = a_game
        self._players_list = a_game.get_players_list()
        self._leading_player = a_game.get_leading_player()
        self.__file_out_data =[] # This is updated every trick!
        #^ This needs to not be reset between rounds, since it's tracking data between rounds! So it doesn't go in the set_initial_values_method
        self._player_score_history = []
        #^ This is a list to which the list of scores for each player at the end of each round will be appended
        # Not using numpy arrays here because the number of rounds/game is nondeterministic
        # NOTE: The score history will be pushed to file at the end of every trick, but only updated on each round
        self.set_initial_values()

    def set_initial_values(self):
        self._winner_of_first_trick = None
        self._trick_history = np.zeros((4,8,32),dtype=np.int8)
        self._call_matrix = np.zeros((4,8),dtype=np.int8)
        self._current_trick = Trick(self)
        for player_index in range(4):
            self._call_matrix[player_index][Calls.none.value] = 1
        self._trick_winners_list = np.zeros((8),dtype=np.int8)
        self.__player_partners = np.zeros((4,4),dtype=np.int8)
        # ^This is needed to provide the ML Agent a correct value to train the partner prediction against
        self.__player_partner_prediction_history = np.zeros((4,4,8),dtype=np.float64)
        #^ This tracks asking_players analyisis of the likelyhood of target player being their partner across each trick
        self.__trick_point_history = np.zeros((4,8),dtype=np.int8)
        #^ This tracks the change in points per player
        self._player_point_history = np.zeros((4,8),dtype=np.int8)
        #^ This tracks the point totals per player

        self.__file_out_data_instance = {"trick_history":self._trick_history,
                     "trick_point_history":self.__trick_point_history,
                     "player_partners":self.__player_partners,
                     "call_matrix":self._call_matrix,
                     "player_point_history":self._player_point_history,
                     "player_partner_prediction_history":self.__player_partner_prediction_history,
                     "player_score_history":self._player_score_history}
                     # TODO make this store the cards in the players hands
        self._trick_count = 0
        self._cards_played_binary = 0

    def get_player_binary_card_state(self, a_player_id):
        #This method should return the binary card state of the cards the player
        #with the matching player id has played
        return self.get_players_list()[a_player_id].get_cards_played() #This is a binary number representing the cards a player has played

    def get_cards_played(self):
        #This method should return a binary number representing the cards played in the round.
        #Can I use the trick history to somehow do this?
        return self._cards_played_binary

    def _get_player_partners(self):
        return self.__player_partners

    def _get_potential_partners_history(self):
        return self.__player_partner_prediction_history

    def _get_point_history(self):
        return self.__trick_point_history

    def get_trick_winners_list(self):
        return self._trick_winners_list

    def _get_file_out_data(self):
        return self.__file_out_data

    def get_current_trick(self):
        return self._current_trick

    def set_current_trick(self, trick):
        self._current_trick = trick

    def get_trick_history(self): #the trick history should only be set by actually playing tricks out
        return self._trick_history

    def get_parent_game(self):
        return self._parent_game

    def set_parent_game(self, game):
        self._parent_game = game

    def get_players_list(self):
        return self._players_list

    def set_players_list(self, players_list):
        self._players_list = players_list

    def get_call_matrix(self):
        return self._call_matrix

    def set_call_matrix(self, calls):
        self._call_matrix = calls

    def get_leading_player(self):
        return self._leading_player

    def set_leading_player(self, player):
        self._leading_player = player

    def get_suit_lead(self):
        return self._current_trick.get_suit_lead()

    def get_file_out_name(self):
        return self._file_out_name

    def set_file_out_name(self, file_name):
        self._file_out_name = file_name

    def get_first_trick_winner(self):
        return self._winner_of_first_trick

    def clear_file_out_history(self):
        self.__file_out_data.clear()

    def notify_players_of_played_card(self):
        for player in self._players_list:
            player.determine_valid_play_list()

    def on_trick_end(self, winning_player, points_on_trick, card_list): #winning player is the player object here
        if self._winner_of_first_trick is None:
            self._winner_of_first_trick = winning_player
        for card in card_list:
            self._cards_played_binary += 1<<card.get_card_id()
            player_number = card.get_owning_player()
            self._trick_history[player_number][self._trick_count][card.get_card_id()] = 1
        self._trick_winners_list[self._trick_count] = winning_player.get_player_id()
        winning_player.set_trick_points(points_on_trick)
        winning_player.set_round_points(winning_player.get_round_points() + points_on_trick)
        self.__trick_point_history[winning_player.get_player_id()][self._trick_count] = points_on_trick
        for i in range(len(self._players_list)):
            self._players_list[i].determine_potential_partners()
            self._player_point_history[i][self._trick_count] = self._players_list[i].get_round_points()

        self.update_player_partner_prediction_history()
        self.__file_out_data.append(copy.deepcopy(self.__file_out_data_instance))
        # by making a copy of the data we'll have a history of how it's changed with each trick
        # using deep copy here to actually duplicate the data and not just link to it's location in memory
        self._trick_count += 1
        if self._trick_count == 8:
            self.on_round_end()

    def update_player_score_history(self, scores_to_be_added):
        self._player_score_history.append(scores_to_be_added)

    def update_player_partner_prediction_history(self):
        for player_number in range(4):
            for target_player in range(4): # this nested loop will query each player for their prediction about their partner status with the target player
                self.__player_partner_prediction_history[player_number][target_player][self._trick_count] = self._players_list[player_number].get_potential_partners_list()[target_player]

    def update_player_partners_history(self):
        # Since this data is only used in training the ML Agent it can be retroactively updated to the correct values
        self.__player_partners = self.__player_partner_prediction_history[-1]
        for instance in self.__file_out_data:
            instance["player_partners"] = self.__player_partners

    def on_round_end(self):
        self._parent_game.update_scores()
        self._file_out_name = str(datetime.datetime.now()).replace(":",";").replace(".",",") + "_game_id_" + str(self._parent_game.get_game_id()) + ".spzd" # files will the named with the date and time of creation and the game id number
        for i in range(4):
            self._players_list[i].set_initial_values()
        self._leading_player = self._players_list[(self._leading_player.get_player_id() + 1)%4]

    def push_data_to_file(self): #need to think about this more to know what info will be needed by the learned agent TODO
        self.__file_out_data.append(copy.deepcopy(self.__file_out_data_instance))
        self.update_player_partners_history()
        if not os.path.isfile(self._file_out_name):
            with open(self._file_out_name, 'wb+') as data_file:
                pickle.dump(self.__file_out_data, data_file)
            # TODO Make sure this contains all the data that we want it to

    def update_call(self, player_id, call_index):
        for index in range(8):
            self._call_matrix[player_id][index] = 0
        self._call_matrix[player_id][call_index] = 1

    def begin_play(self): #this method should start asking players to play cards to the active trick while they can do so
        for i in range(4):
            self._players_list[i].ask_for_call()
            if sum(self._call_matrix[i][1:]) != 0:
                break
        while self._leading_player.does_play_continue():
            for player in self._players_list:
                player.play_card_to(self._current_trick)

    def get_game_state_for_player(self, a_player_index): #this method should return the current game state from the given players prespective for use in the ML agent
        a_game_state = {}
        a_game_state["trick history"] = self._trick_history
        a_game_state["trick_point_history"] = self.__trick_point_history
        a_game_state["call_matrix"] = self._call_matrix
        a_game_state["current_trick"] = self._current_trick
        a_game_state["current_player"] = self._players_list[a_player_index] # used for getting info about the players cards from their hand
        return a_game_state
        #TODO Consider what else need to go in here
