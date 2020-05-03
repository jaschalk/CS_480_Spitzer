import unittest
import copy
import numpy as np
import pickle
from agents.RandomAgent import RandomAgent
from unit_tests.Setup import general_setup
from game_objects.Round import Round
from game_objects.Player import Player
from game_objects.Deck import Deck
from game_objects.Trick import Trick
from game_objects.Card import Card
from game_objects.Game import Game

class RoundTest(unittest.TestCase):

    def setUp(self):
        setup_results = general_setup()
        self.temp_game = setup_results["active_game"]
        self.temp_players = setup_results["list_of_players"]
        self.test_round = setup_results["current_round"]
        self.temp_trick = setup_results["current_trick"]
        self.temp_deck = setup_results["game_deck"]
        del setup_results

    def test_init(self):
        self.assertIsInstance(self.test_round.get_current_trick(), Trick)
        trick_history = self.test_round.get_trick_history()
        self.assertEqual(len(trick_history),4)
        self.assertEqual(len(trick_history[0]),8)
        self.assertEqual(len(trick_history[0][0]),32)
        self.assertEqual(len(self.test_round.get_players_list()), 4)
        self.assertEqual(len(self.test_round._get_player_partners()), 4)
        self.assertEqual(len(self.test_round._get_player_partners()[0]), 4)
        self.assertEqual(len(self.test_round.get_call_matrix()), 4)
        self.assertEqual(len(self.test_round.get_call_matrix()[0]), 8)
        for row in range(4):
            for col in range(8):
                if col == 0:
                    self.assertEqual(self.test_round.get_call_matrix()[row][col], 1)
                else:
                    self.assertEqual(self.test_round.get_call_matrix()[row][col], 0)

    def test_on_trick_finish(self):
        self.test_round.set_leading_player(self.temp_players[3])
        initial_card_count = 0
        for i in range(4):
            Card(12-i, "clubs").visit(self.temp_players[i])
            initial_card_count += len(self.temp_players[i].get_hand().get_cards_in_hand())
        for i in range(4):
            self.temp_players[i].get_hand().play_card_at_index(self.temp_trick, 0)
        post_trick_card_count = 0
        for i in range(4):
            post_trick_card_count += len(self.temp_players[i].get_hand().get_cards_in_hand())
        self.assertEqual(initial_card_count, post_trick_card_count+4)
        for i in range(4):
            self.assertEqual(self.test_round.get_trick_history()[i][0][Card(12-i, "clubs").get_card_id()], 1)
            #The 3rd player will have played the Ace of Clubs, the 2nd player the 10 of Clubs, the 1st the King of Clubs, the 0th the 9 of Clubs
        self.assertEqual(self.test_round.get_leading_player(), self.temp_players[3])
        self.assertEqual(self.test_round._get_point_history()[3][0], 25)

    def test_potential_partners_history(self):
        for i in range(4): # (P0, QC), (P1, 7D), (P2, QS), (P3, QH)
            Card(i, "trump").visit(self.temp_players[i])
        for i in range(4):
            self.temp_players[i].get_hand().play_card_at_index(self.temp_trick, 0)
        self.assertEqual(self.test_round._get_potential_partners_history()[0][2][0], 1)
        self.assertEqual(self.test_round._get_potential_partners_history()[1][3][0], 1)
        self.assertEqual(self.test_round._get_potential_partners_history()[2][0][0], 1)
        self.assertEqual(self.test_round._get_potential_partners_history()[3][1][0], 1)

    def test_on_round_finish(self):
        initial_player_points = []
        for player in self.temp_players:
            player.set_controlling_agent(RandomAgent())
            self.temp_deck.deal_cards_to(player)
            initial_player_points.append(player.get_round_points())
        self.test_round.begin_play()
        self.assertEqual(len(self.temp_deck.get_card_list()), 0)

    def test_update_trick_winners_list(self):
        for i in range(4): # (P0, QC), (P1, 7D), (P2, QS), (P3, QH)
            Card(i, "trump").visit(self.temp_players[i])
        for i in range(4):
            self.temp_players[i].get_hand().play_card_at_index(self.temp_trick, 0)
        self.assertEqual(self.test_round.get_trick_winners_list()[0], 0)
        for i in range(4):
            self.temp_players[i].set_initial_values()
        for i in range(4):
            Card(12-i, "hearts").visit(self.temp_players[i])
        for i in range(4):
            self.temp_players[i].get_hand().play_card_at_index(self.temp_trick, 0)
        self.assertEqual(self.test_round.get_trick_winners_list()[1], 3)

    def test_file_out_behavior(self):
        for player in self.temp_players:
            player.set_controlling_agent(RandomAgent())
        self.temp_game.play_game()
        with open(self.test_round.get_file_out_name(), 'rb') as input:
            file_data = pickle.load(input)
            for i in range(len(file_data)):
                self.assertTrue(self.test_round._get_file_out_data()[i]["trick_history"].all() == file_data[i]["trick_history"].all())
                self.assertGreater(self.test_round._get_file_out_data()[i]["trick_history"].sum(), 0)
                self.assertTrue(self.test_round._get_file_out_data()[i]["trick_point_history"].all() == file_data[i]["trick_point_history"].all())
                self.assertGreaterEqual(self.test_round._get_file_out_data()[i]["trick_point_history"].sum(), 0)
                self.assertTrue(self.test_round._get_file_out_data()[i]["player_partners"].all() == file_data[i]["player_partners"].all())
                self.assertGreater(self.test_round._get_file_out_data()[i]["player_partners"].sum(), 0)
                self.assertTrue(self.test_round._get_file_out_data()[i]["call_matrix"].all() == file_data[i]["call_matrix"].all())
                self.assertGreater(self.test_round._get_file_out_data()[i]["call_matrix"].sum(), 0)
                self.assertTrue(self.test_round._get_file_out_data()[i]["player_cards_in_hand_history"].all() == file_data[i]["player_cards_in_hand_history"].all())
                self.assertGreater(self.test_round._get_file_out_data()[i]["player_cards_in_hand_history"].sum(), 0)
                self.assertTrue(self.test_round._get_file_out_data()[i]["player_point_history"].all() == file_data[i]["player_point_history"].all())
                self.assertGreater(self.test_round._get_file_out_data()[i]["player_point_history"].sum(), 0)
                self.assertTrue(self.test_round._get_file_out_data()[i]["player_partner_prediction_history"].all() == file_data[i]["player_partner_prediction_history"].all())
                for e in range(len(file_data[i]["player_score_history"])):
                    self.assertTrue(self.test_round._get_file_out_data()[i]["player_score_history"][e] == file_data[i]["player_score_history"][e])

    def tearDown(self):
        for player in self.temp_players:
            del player
        del self.temp_players
        del self.test_round
        del self.temp_game
        del self.temp_trick
        del self.temp_deck

if __name__ == "__main__":
    unittest.main()