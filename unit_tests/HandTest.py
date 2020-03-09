import unittest
from unit_tests.Setup import general_setup

class HandTest(unittest.TestCase):

    def setUp(self):
        setup_results = general_setup()
        self.temp_game = setup_results["active_game"]
        self.temp_deck = setup_results["game_deck"]
        self.temp_player = setup_results["list_of_players"][0]
        self.temp_round = setup_results["current_round"]
        self.test_hand = setup_results["player_zero_hand"]
        self.temp_trick = setup_results["current_trick"]

    def test_on_init(self):
        self.assertEqual(len(self.test_hand.get_cards_in_hand()), 0)
        self.assertEqual(len(self.test_hand.get_valid_play_list()), 0)

    def test_on_deal(self):
        self.temp_player.hand = self.test_hand
        self.temp_deck.deal_cards_to(self.temp_player)
        self.assertEqual(len(self.test_hand.get_cards_in_hand()), 8)

    def test_card_played(self):
        self.temp_round.set_leading_player(self.temp_player)
        self.temp_deck.deal_cards_to(self.temp_player)
        start_hand_size = len(self.test_hand.get_cards_in_hand())
        self.test_hand.determine_valid_play_list()
        start_valid_list_size = len(self.test_hand.get_valid_play_list())
        self.test_hand.play_card_at_index(self.temp_trick, 0)
        self.assertEqual(len(self.test_hand.get_cards_in_hand()), start_hand_size - 1)
        self.test_hand.determine_valid_play_list()
        self.assertEqual(len(self.test_hand.get_valid_play_list()), start_valid_list_size - 1)

    def tearDown(self):
        self.test_hand.get_cards_in_hand().clear()
        self.test_hand.get_valid_play_list().clear()
        del self.test_hand

if __name__ == "__main__":
    unittest.main()