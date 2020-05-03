import unittest
from unit_tests.Setup import general_setup
from game_objects.Hand import Hand
from game_objects.Card import Card

class PlayerTest(unittest.TestCase):

    def setUp(self):
        setup_results = general_setup()
        self.temp_player_list = setup_results["list_of_players"]
        self.temp_player_zero = self.temp_player_list[0]
        self.temp_round = setup_results["current_round"]
        self.test_hand = setup_results["player_zero_hand"]
        self.current_trick = setup_results["current_trick"]

    def test_on_init(self):
        self.assertEqual(self.temp_player_zero.get_round_points(), 0)
        self.assertEqual(self.temp_player_zero.get_total_score(), 0)
        self.assertFalse(self.temp_player_zero.get_is_leading())
        self.assertIsInstance(self.temp_player_zero.get_hand(), Hand)
        self.assertEqual(len(self.temp_player_zero.get_valid_call_list()), 8)
        self.assertEqual(len(self.temp_player_zero.get_potential_partners_list()), 4)
        self.assertEqual(self.temp_player_zero.get_potential_partners_list()[0], 1)
        for index in range(1,4):
            self.assertAlmostEqual(self.temp_player_zero.get_potential_partners_list()[index], 1/3)

    def test_trick_complete(self):
        current_round_points = self.temp_player_zero.get_round_points()
        for index in range(4):
            Card(index, "trump").visit(self.temp_player_list[index])
        for index in range(4):
            self.temp_player_list[index].get_hand().play_card_at_index(self.current_trick, 0)
        self.assertEqual(self.temp_player_zero.get_round_points(), 9)
        self.assertEqual(self.temp_player_zero.get_round_points(), (current_round_points + self.temp_player_zero.get_trick_points()))
        self.assertEqual(self.temp_player_list[0].get_potential_partners_list(), [1,0,1,0])
        self.assertEqual(self.temp_player_list[1].get_potential_partners_list(), [0,1,0,1])
        self.assertEqual(self.temp_player_list[2].get_potential_partners_list(), [1,0,1,0])
        self.assertEqual(self.temp_player_list[3].get_potential_partners_list(), [0,1,0,1])

    def test_card_acceptance(self):
        temp_card = None
        for index in range(5):
            temp_card = Card(index, "trump")
            temp_card.visit(self.temp_player_zero)
        self.assertEqual(self.temp_player_zero.get_hand().get_cards_in_hand()[4], temp_card)

    def test_no_call_is_made(self):
        self.assertEqual(self.temp_player_zero.get_potential_partners_list()[0], 1)
        for index in range(1,4):
            self.assertAlmostEqual(self.temp_player_zero.get_potential_partners_list()[index], 1/3)

    def tearDown(self):
        del self.temp_player_list

if __name__ == "__main__":
    unittest.main()