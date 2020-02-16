import pickle
import numpy as np
import copy
import os

class Round:

    current_trick = None
    parent_game = None
    leading_player = None
    players_list = [None, None, None, None]
    #using numpy's arrays rather than standard python lists since this is the data that will be interfacing with the ML process
    trick_history = np.zeros((4,8,32),dtype=np.int8)
    player_partners = np.zeros((4,4),dtype=np.int8)
    call_matrix = np.zeros((4,8),dtype=np.int8)
    player_score_history = np.zeros((4,8),dtype=np.int8)
    player_partner_prediction_history = np.zeros((4,4,8),dtype=np.float64)
    trick_point_history = np.zeros(8,dtype=np.int8)
    #the values in the file_out_data dict are mutable so changes to the variables will be reflected here
    file_out_data_instance = {"trick_history":trick_history,
                     "trick_point_history":trick_point_history,
                     "player_partners":player_partners,
                     "call_matrix":call_matrix,
                     "player_score_history":player_score_history,
                     "player_partner_prediction_history":player_partner_prediction_history}
    file_out_data = []
    trick_count = 0

    def __init__(self, a_game):
        self.parent_game = a_game
        self.players_list = a_game.get_players()
        for i in range(4):
            self.call_matrix[i][0] = 1

    def on_trick_end(self, winning_player, points_on_trick, card_list):
        for card in card_list:
            player_number = card.get_owning_player().get_player_number()
            self.trick_history[player_number][self.trick_count][card.get_index()] = 1
        self.trick_point_history[self.trick_count] = points_on_trick
        for player_number in range(4):
            for target_player in range(4): # this nested loop will query each player for their prediction about their partner status with the target player
                self.player_partner_prediction_history[player_number][target_player][self.trick_count] = self.players_list[player_number].get_partners_list()[target_player]
                #this could stand to be rewritten to be more readable
        self.file_out_data.append(copy.deepcopy(self.file_out_data_instance)) #by making a copy of the data we'll have a history of how it's changed with each trick
                                    # using deep copy here to actually duplicate the data and not just link to it's location in memory
        self.trick_count += 1

    def on_round_end(self):
        #update player scores
        #have the game check if the game is over
        #other stuff?
        pass

    def push_data_to_file(self, file_name): #need to think about this more to know what info will be needed by the learned agent
        if not os.path.isfile(file_name):
            with open(file_name, 'wb') as data_file:
                pickle.dump(self.file_out_data, data_file)
