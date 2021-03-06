import unittest
from unit_tests.Setup import general_setup
from game_objects.Trick import Trick
from game_objects.Player import Player
from game_objects.Card import Card
from game_objects.Round import Round

class TrickTest(unittest.TestCase):

    def setUp(self):
        setup_results = general_setup()
        self.testTrick = setup_results["current_trick"]
        self.tempPlayers = setup_results["list_of_players"]
        for i in range(4):
            Card(9+i, "hearts").visit(self.tempPlayers[i])
        del setup_results

    def test_on_init(self):
        for card in self.testTrick.get_played_cards_list():
            self.assertIs(card, Card(-1,"null"))
        self.assertIsNone(self.testTrick.get_suit_lead())
        self.assertIsNotNone(self.testTrick.get_parent_round())
        self.assertIsNone(self.testTrick.get_winning_player())
        self.assertEqual(self.testTrick.get_points_on_trick(), 0)

    def test_on_accept_card(self):
        card_is_none_count = 0
        self.tempPlayers[2].get_hand().get_cards_in_hand().pop() # This is currently making the hand binary value incorrect
        Card(0, "trump").visit(self.tempPlayers[2])
        self.tempPlayers[0].get_hand().play_card_at_index(self.testTrick, 0)
        self.assertIsNotNone(self.testTrick.get_played_cards_list()[0])
        self.assertEqual(self.testTrick.get_suit_lead(), "hearts")
        self.assertEqual(self.testTrick.get_winning_player(), self.tempPlayers[0])
        self.tempPlayers[1].get_hand().play_card_at_index(self.testTrick, 0)
        for card in self.testTrick.get_played_cards_list():
            if card is Card(-1,"null"):
                card_is_none_count += 1
        self.assertEqual(card_is_none_count, 2)
        
        self.assertEqual(self.testTrick.get_suit_lead(), "hearts")
        self.assertEqual(self.testTrick.get_winning_player(), self.tempPlayers[0])
        self.tempPlayers[2].get_hand().play_card_at_index(self.testTrick, 0)
        self.assertEqual(self.testTrick.get_suit_lead(), "hearts")
        self.assertEqual(self.testTrick.get_winning_player(), self.tempPlayers[2])

    def test_on_fill(self):
        for i in range(4):
            self.tempPlayers[i].get_hand().play_card_at_index(self.testTrick, 0)
        self.assertEqual(self.testTrick.get_winning_card(), Card(-1, "null"))
        for i in range(4):
            self.assertIs(self.testTrick.get_played_cards_list()[i], Card(-1,"null"))
        self.assertEqual(self.testTrick.get_points_on_trick(), 0)

    def tearDown(self):
        for player in self.tempPlayers:
            del player
        del self.tempPlayers
        del self.testTrick

if __name__ == "__main__":
    unittest.main()