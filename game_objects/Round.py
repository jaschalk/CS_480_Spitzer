import pickle
import numpy as np
import copy
import os
import datetime
from enums import Calls
from game_objects.Trick import Trick
from agents.LearningAgent import Agent
from game_objects.Card import Card

class Round:
    '''
    The Round class is used to coordinates communication between the trick and the players,
    notify other objects of game state changes, and log game data to output files.
    '''

    def __init__(self, a_game):
        self._parent_game = a_game
        self._players_list = a_game.get_players_list()
        self._leading_player = a_game.get_leading_player()
        self._starting_player = self._leading_player
        self.__file_out_data =[]
        #^ This needs to not be reset between rounds, since it's tracking data between rounds! So it doesn't go in the set_initial_values_method
        self._player_score_history = []
        self._current_trick = Trick(self)
        # NOTE: The score history will be pushed to file at the end of every trick, but only updated on each round
        self.set_initial_values()

    def set_initial_values(self):
        # This method is called at the start of each round
        self._winner_of_first_trick = None
        self._trick_history = np.zeros((4,8,32),dtype=np.int8)
        self._call_matrix = np.zeros((4,8),dtype=np.int8)
    #NOTE publish subscribe code spike
        self._current_trick.log_subscriber_to_message(self, "print_test", "print_test")
        self._current_trick.log_subscriber_to_message(self, "print_message", "print_message")
#        self._current_trick.notify_subscribers()
        self._current_trick.print_message("This is the message")
    #NOTE publish subscribe code spike
        for player_index in range(4):
            self._call_matrix[player_index][Calls.none.value] = 1
        self._trick_winners_list = np.zeros((8),dtype=np.int8)
        self.__player_cards_in_hand_history = np.zeros((4,8,32), dtype=np.int8)
        self.__player_partners = np.zeros((4,4),dtype=np.int8)
        self.__player_partner_prediction_history = np.zeros((4,4,8),dtype=np.float64)
        self.__trick_point_history = np.zeros((4,8),dtype=np.int8)
        #^ This tracks the change in points per player
        self._player_point_history = np.zeros((4,8),dtype=np.int8)
        #^ This tracks the point totals per player

        self.__file_out_data_instance = {"trick_history":self._trick_history,
                     "trick_point_history":self.__trick_point_history,
                     "player_partners":self.__player_partners,
                     "call_matrix":self._call_matrix,
                     "player_cards_in_hand_history":self.__player_cards_in_hand_history,
                     "player_point_history":self._player_point_history,
                     "player_partner_prediction_history":self.__player_partner_prediction_history,
                     "player_score_history":self._player_score_history}
        self._trick_count = 0
        self._cards_played_binary = 0

    def get_player_binary_card_state(self, a_player_id):
        #This is a binary number representing the cards a player has played
        return self.get_players_list()[a_player_id].get_cards_played() 
        
#NOTE publish subscribe code spike
    def print_test(self, a_message):
        pass
#        print("test")

    def print_message(self, a_message):
        pass
#        print(f"The Round is printing: {a_message}")
#NOTE publish subscribe code spike

    def get_cards_played(self):
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

    def get_trick_history(self):
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

    def update_player_cards_in_hand_history_for_player(self, a_player):
        cards_in_hand = a_player.get_cards_in_hand()
        for card in cards_in_hand:
            self.__player_cards_in_hand_history[a_player.get_player_id()][self._trick_count][card.get_card_id()] = 1

    def notify_players_of_played_card(self):
        cards_on_trick = self._current_trick.get_played_cards_list()
        players_already_played = [card.get_owning_player() for card in cards_on_trick if card is not None]
        for player in self._players_list:
            if player.get_player_id() not in players_already_played:
                player.determine_valid_play_list()

    def on_trick_end(self, winning_player, points_on_trick, card_list): #winning player is the player object here
        if self._winner_of_first_trick is None:
            self._winner_of_first_trick = winning_player
        self._trick_winners_list[self._trick_count] = winning_player.get_player_id()
        winning_player.set_trick_points(points_on_trick)
        winning_player.set_round_points(winning_player.get_round_points() + points_on_trick)
        self.__trick_point_history[winning_player.get_player_id()][self._trick_count] = points_on_trick
        for card in self._current_trick.get_played_cards_list():
            if card is not None:
                self._cards_played_binary += 1<<card.get_card_id()
                player_number = card.get_owning_player()
                self._trick_history[player_number][self._trick_count][card.get_card_id()] = 1
        for i in range(len(self._players_list)):
            self._players_list[i].determine_potential_partners()
            self._player_point_history[i][self._trick_count] = self._players_list[i].get_round_points()
            self._players_list[i].initialze_valid_play_list()
        self.update_player_partner_prediction_history()
        self.__file_out_data.append(copy.deepcopy(self.__file_out_data_instance))
        self._trick_count += 1
        for player in self._players_list:
            player.learn()
        self._leading_player = winning_player
        if self._trick_count == 8:
            self.on_round_end()
        else:
            for player in self._players_list:
                self.update_player_cards_in_hand_history_for_player(player)

    def update_player_score_history(self, scores_to_be_added):
        self._player_score_history.append(scores_to_be_added)

    def update_player_partner_prediction_history(self):
        for player_number in range(4):
            for target_player in range(4):
                self.__player_partner_prediction_history[player_number][target_player][self._trick_count] \
                    = self._players_list[player_number].get_potential_partners_list()[target_player]

    def update_player_partners_history(self):
        self.__player_partners = self.__player_partner_prediction_history[-1]
        for instance in self.__file_out_data:
            instance["player_partners"] = self.__player_partners

    def inform_learning_agents_of_round_end(self):
        learning_agent_indices = [index for index in range(len(self._players_list)) 
                                    if isinstance(self._players_list[index].get_controlling_agent(), Agent)]
        for ML_index in learning_agent_indices:
            other_players_calls = []
            for i in range(4):
                if i != ML_index:
                    other_players_calls.append(sum(self._call_matrix[i][5:]))
            if sum(other_players_calls) == 0:
                call_list = self._call_matrix[ML_index]
                call_index = [index for index in range(len(call_list)) if call_list[index] == 1][0]

                ML_player = self._players_list[ML_index]
                reward = ML_player.get_score_change_list()[-1]
                if reward == 0 and call_index > 4:
                    reward = -1*self._players_list[(ML_index+1)%4].get_score_change_list()[-1]
                self._players_list[ML_index].get_controlling_agent().store_call_mem_transition(ML_player.get_starting_cards(), call_index, reward)
#            self._players_list[ML_index].get_controlling_agent().train_call_generator()
            # This got commented out since we're not using the learning call method right now.

    def on_round_end(self):
        self._parent_game.update_scores()
        self.inform_learning_agents_of_round_end()
        self._file_out_name = str(self._parent_game.get_game_id()) + ".spzd"
        for i in range(4):
            self._players_list[i].set_initial_values()
        self._starting_player = self._players_list[(self._starting_player.get_player_id() + 1)%4]

    def push_data_to_file(self):
        self.__file_out_data.append(copy.deepcopy(self.__file_out_data_instance))
        self.update_player_partners_history()
        if not os.path.isfile(self._file_out_name):
            with open(self._file_out_name, 'wb+') as data_file:
                pickle.dump(self.__file_out_data, data_file)

    def update_call(self, player_id, call_index):
        for index in range(8):
            self._call_matrix[player_id][index] = 0
        self._call_matrix[player_id][call_index] = 1

    def begin_play(self):
        for i in range(4):
            self._players_list[i].ask_for_call()
            if sum(self._call_matrix[i][1:]) != 0:
                break
        while self._leading_player.does_play_continue():
            self.play_trick()

    def play_trick(self):
        play_order_list = [self._players_list[(index+self._leading_player.get_player_id())%4] 
                            for index in range(len(self._players_list))]
        for player in play_order_list:
            player.play_card_to(self._current_trick)

    def get_game_state_for_player(self, a_player_index):
        a_game_state = {}
        a_game_state["trick_history"] = self._trick_history
        a_game_state["trick_point_history"] = self.__trick_point_history
        a_game_state["call_matrix"] = self._call_matrix
        a_game_state["current_trick"] = self._current_trick
        a_game_state["current_player"] = self._players_list[a_player_index]
        return a_game_state

    def get_game_state_for_play_card(self, a_player_index):
        game_state = np.zeros((1, 1228), dtype=np.float32)
        index_of_write = 0
        #   The cards in hand, (This would be a 32 element list)
        for card in self._players_list[a_player_index].get_cards_in_hand(): # this isn't filtering by valid or not
            game_state[0][card.get_card_id()] = 1
        index_of_write = 32

        #   The cards played to the trick so far, (4*32 element list)
        for card in self._current_trick.get_played_cards_list():
            if card is not Card(-1,"null"):
                game_state[0][index_of_write + card.get_card_id()] = 1
            index_of_write += 32

        #   The players potential partners list, (4 element list)
        for i in range(4):
            game_state[0][index_of_write] = self._players_list[a_player_index].get_potential_partners_list()[i]
            index_of_write += 1

        #   The list of cards played so far, (4*8*32 elements)
        for player_num in range(4):
            for trick_num in range(8):
                for card_num in range(32):
                    game_state[0][index_of_write] = self._trick_history[player_num][trick_num][card_num]
                    index_of_write += 1

        #   The call state of the game, (This would be a 4*8 element list)
        for player_num in range(4):
            for call_num in range(8):
                game_state[0][index_of_write] = self._call_matrix[player_num][call_num]
                index_of_write += 1

        #   The normalized list of points taken by each player (4 elements)
        # TODO: Can we change this to the points taken by each team?
        normalized_player_point_list = [player.get_round_points()/120 for player in self._players_list]
        for player_num in range(4):
            game_state[0][index_of_write] = normalized_player_point_list[player_num]
            index_of_write += 1

        #   The normailzed score list for each player (4 elements)
        normalized_player_score_list = [player.get_total_score()/120 for player in self._players_list]
        for player_num in range(4):
            game_state[0][index_of_write] = normalized_player_score_list[player_num]
            index_of_write += 1

        return game_state