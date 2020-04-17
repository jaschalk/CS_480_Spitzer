import unittest
from unit_tests.Setup import general_setup
from game_objects.Deck import Deck
from game_objects.CallRules import CallRules
from game_objects.CardRuleTree import CardRuleTree
from game_objects.PartnerRuleTree import PartnerRuleTree
from agents.RandomAgent import RandomAgent
from agents.CustomAgent import CustomAgent
from agents.LearningAgent import Agent

class GameTest(unittest.TestCase):

    number_of_games_to_be_played = 1

    def setUp(self):
        setup_results = general_setup()
        self.temp_game = setup_results["active_game"]
        self.temp_deck = setup_results["game_deck"]
        self.temp_player_list = setup_results["list_of_players"]
        self.temp_round = setup_results["current_round"]
        del setup_results

    def test_on_init(self):
        self.assertEqual(len(self.temp_player_list), 4)
        self.assertIsInstance(self.temp_deck, Deck)
        self.assertIsInstance(self.temp_game.get_card_rules(), CardRuleTree)
        self.assertIsInstance(self.temp_game.get_partner_rules(), PartnerRuleTree)
        self.assertIsInstance(self.temp_game.get_call_rules(), CallRules)

    def test_deal_cards(self):
        temp_player = self.temp_player_list[0]
        self.temp_deck.deal_cards_to(temp_player)
        self.assertEqual((len(self.temp_deck.get_card_list()) + len(temp_player.get_cards_in_hand())), 32)

    def test_end_game_one_winner(self):
        self.temp_player_list[0].set_total_score(42)
        self.temp_player_list[1].set_total_score(30)
        self.temp_player_list[2].set_total_score(28)
        self.temp_player_list[3].set_total_score(20)
        self.assertEqual(self.temp_game.which_player_wins(), 0)

    def test_end_game_tie(self):
        self.temp_player_list[0].set_total_score(42)
        self.temp_player_list[1].set_total_score(42)
        self.temp_player_list[2].set_total_score(28)
        self.temp_player_list[3].set_total_score(20)
        self.assertEqual(self.temp_game.which_player_wins(), -1)

    def test_end_game_continues(self):
        self.temp_player_list[0].set_total_score(36)
        self.temp_player_list[1].set_total_score(30)
        self.temp_player_list[2].set_total_score(28)
        self.temp_player_list[3].set_total_score(20)
        self.assertEqual(self.temp_game.which_player_wins(), -1)

    def test_update_scores(self):
        for player in self.temp_player_list:
            player.set_controlling_agent(RandomAgent())
        self.temp_game.begin_round()
        self.assertNotEqual(sum(self.temp_game.get_score_list()), 0)

    def test_play_game(self):
        for player in self.temp_player_list:
            player.set_controlling_agent(RandomAgent())
        self.temp_game.play_game()
        self.assertGreaterEqual(max(self.temp_game.get_score_list()), 42)

    def test_play_multiple_games(self):
        self.tearDown()
        for i in range(self.number_of_games_to_be_played):
#            print("Game number " + str(i))
            self.setUp()
            self.test_play_game()

    def test_play_with_custom_agent(self):
        for player in self.temp_player_list:
            player.set_controlling_agent(CustomAgent())
        self.temp_game.play_game()
        self.assertGreaterEqual(max(self.temp_game.get_score_list()), 42)

    def test_play_multiple_games_with_custom_agent(self):
        self.tearDown()
        for i in range(self.number_of_games_to_be_played):
#            print("Game number w/ custom " + str(i))
            self.setUp()
            self.test_play_with_custom_agent()

    def test_play_with_learning_agent(self):
        self.temp_player_list[0].set_controlling_agent(Agent(lr=0.001, gamma=0.9, n_actions=8, epsilon=0, batch_size=64,
                                                input_dims=[1228], epsilon_dec=1e-4, epsilon_min=1e-3,
                                                mem_size=100000, fname="network_test.h5", fc1_dims=128, 
                                                fc2_dims=128, replace=100))
        for index in range(1,4):
            self.temp_player_list[index].set_controlling_agent(CustomAgent)
        self.temp_game.play_game()
        self.assertGreaterEqual(max(self.temp_game.get_score_list()), 42)

    def tearDown(self):
        del self.temp_game
        del self.temp_deck
        del self.temp_player_list
        del self.temp_round

if __name__ == "__main__":
    unittest.main()