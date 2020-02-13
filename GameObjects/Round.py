import pickle
import numpy as np
import os

class Round:

    current_trick = None
    parent_game = None
    players_list = [None, None, None, None]
    trick_history = np.zeros((4,8,32))
    player_partners = np.zeros((4,4))
    call_matrix = [[1,0,0,0,0,0,0,0],
                   [1,0,0,0,0,0,0,0],
                   [1,0,0,0,0,0,0,0],
                   [1,0,0,0,0,0,0,0]]
    player_score_history = np.zeros((4,8))
    leading_player = None
    trick_point_history = []
    #the values in the file_out_data dict are mutable so changes to the variables will be reflected here
    file_out_data = {"trick_history":trick_history,
                     "player_partners":player_partners,
                     "call_matrix":call_matrix,
                     "player_score_history":player_score_history}
    trick_count = 0

    def __init__(self, a_game):
        self.parent_game = a_game
        self.players_list = a_game.get_players()

    def on_trick_end(self, winning_player, points_on_trick, card_list):
        for card in card_list:
            player_number = card.get_owning_player().get_player_number()
            self.trick_history[player_number][self.trick_count][card.get_index()] = 1
        self.trick_point_history.append(points_on_trick)
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
