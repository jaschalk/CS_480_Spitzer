import pickle
import numpy as np
import copy
import os
from game_objects.Trick import Trick

class Round:

    #Might want to add a get game state method to the round for use in the agent.

    _current_trick = None
    _parent_game = None
    _leading_player = None
    _winner_of_first_trick = None
    _players_list = [None, None, None, None]
    #using numpy's arrays rather than standard python lists since this is the data that will be interfacing with the ML process
    _trick_history = np.zeros((4,8,32),dtype=np.int8)
    _call_matrix = np.zeros((4,8),dtype=np.int8)
    _player_score_history = np.zeros((4,8),dtype=np.int8)
    __player_partners = np.zeros((4,4),dtype=np.int8) #this is __ to emphasize that the players should at no time have this information
    __player_partner_prediction_history = np.zeros((4,4,8),dtype=np.float64) # __ because it shouldn't be needed anywhere other than this class
    __trick_point_history = np.zeros((4,8),dtype=np.int8) # __ because it shouldn't be needed anywhere other than this class
    #the values in the file_out_data_instance dict are mutable so changes to the variables will be reflected here
    __file_out_data_instance = {"trick_history":_trick_history,
                     "trick_point_history":__trick_point_history,
                     "player_partners":__player_partners,
                     "call_matrix":_call_matrix,
                     "player_score_history":_player_score_history,
                     "player_partner_prediction_history":__player_partner_prediction_history}
    __file_out_data = []
    _file_out_name = ""
    _trick_count = 0

    def __init__(self, a_game):
        self._parent_game = a_game
        self._players_list = a_game.get_players_list()
        self._current_trick = Trick(self)
        for i in range(4):
            self._call_matrix[i][0] = 1

    def get_player_binary_card_state(self, a_player_id):
        #This method should return the binary card state of the cards the player 
        #with the matching player id has played
        return self.get_players_list()[a_player_id].get_cards_played() #This is a binary number representing the cards a player has played

    def get_cards_played(self):
        #This method should return a binary number representing the cards played in the round.
        pass

    def _get_player_partners(self):
        return self.__player_partners

    def _get_potential_partners_history(self):
        return self.__player_partner_prediction_history

    def _get_point_history(self):
        return self.__trick_point_history

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
        print("Incoming player is:")
        print(player)
        self._leading_player = player
        print("New leading Player is:")
        print(self._leading_player)

    def get_suit_lead(self):
        return self._current_trick.get_suit_lead()

    def get_file_out_name(self):
        return self._file_out_name

    def set_file_out_name(self, file_name):
        self._file_out_name = file_name

    def on_trick_end(self, winning_player, points_on_trick, card_list): #is winning player the player object, or their index?
        if self._winner_of_first_trick is None:
            self._winner_of_first_trick = winning_player
        for card in card_list:
            player_number = card.get_owning_player() #this should be changed?
            self._trick_history[player_number][self._trick_count][card.get_card_id()] = 1
        self.__trick_point_history[winning_player.get_player_id()][self._trick_count] = points_on_trick
        self.update_player_partner_prediction_history() #I don't remember how was supposed to work?
        self.__file_out_data.append(copy.deepcopy(self.__file_out_data_instance)) #by making a copy of the data we'll have a history of how it's changed with each trick
                                                                    # using deep copy here to actually duplicate the data and not just link to it's location in memory
        self._trick_count += 1

    def update_player_partner_prediction_history(self):
        #this could stand to be rewritten to be more readable
        for player_number in range(4):
            for target_player in range(4): # this nested loop will query each player for their prediction about their partner status with the target player
                self.__player_partner_prediction_history[player_number][target_player][self._trick_count] = self._players_list[player_number].get_potential_partners_list()[target_player]

    def on_round_end(self):
        points_taken_list = []
        for i in range(4):
            points_taken_list.append(self.__trick_point_history[i][7]) #this should generate a list of the points the players took on this trick in order of player number
        has_ended = self._parent_game.update_scores(points_taken_list) #this feels like it should cause the game to check if the game should end?
        if has_ended:
            self.push_data_to_file("dynamicfilename") #need to come up with a system for knowing what to name the files
        else:
            self._parent_game.start_round()

    def push_data_to_file(self, file_name): #need to think about this more to know what info will be needed by the learned agent
        if not os.path.isfile(file_name):
            with open(file_name, 'wb') as data_file:
                pickle.dump(self.__file_out_data, data_file)

    def update_call(self, player_id, call_index):
        for index in range(8):
            self._call_matrix[player_id][index] = 0
        self._call_matrix[player_id][call_index] = 1

    def begin_play(self): #this method should start asking players to play cards to the active trick while they can do so
        while self._leading_player.does_play_continue():
            for player in self._players_list:
                player.play_card_to(self._current_trick)
        #TODO call push data out

    def get_game_state_for_player(self, a_player_index): #this method should return the current game state from the given players prespective
        a_game_state = {}
        a_game_state["trick history"] = self._trick_history
        a_game_state["trick_point_history"] = self.__trick_point_history
        a_game_state["call_matrix"] = self._call_matrix
        a_game_state["current_trick"] = self._current_trick
        a_game_state["current_player"] = self._players_list[a_player_index]
        #TODO finish this method!
