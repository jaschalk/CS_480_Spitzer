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
            print(self.tempPlayers[i] == setup_results["list_of_players"][i])
        for i in range(4):
            self.tempPlayers[i].accept(Card(9+i, "hearts"))
        del setup_results

    def test_on_init(self):
        for card in self.testTrick.get_played_cards_list():
            self.assertIsNone(card)
        self.assertIsNone(self.testTrick.get_suit_lead())
        self.assertIsNotNone(self.testTrick.get_parent_round())
#        self.assertIsNone(self.testTrick.get_leading_player())
        self.assertIsNone(self.testTrick.get_winning_player())
        self.assertEqual(self.testTrick.get_points_on_trick(), 0)

    def test_on_accept_card(self):
        self.tempPlayers[0].get_hand().play_card_at_index(self.testTrick, 0)
        print("Done with line 27")
        self.assertIsNotNone(self.testTrick.get_played_cards_list()[0])
        self.assertEqual(self.testTrick.get_suit_lead(), "hearts")
        self.assertEqual(self.testTrick.get_winning_player(), self.tempPlayers[0]) # for reasons unknown these are different player objects that have the same id#
        print("Player hand:")
        print(self.tempPlayers[1].get_hand().get_cards_in_hand())
        self.tempPlayers[1].get_hand().play_card_at_index(self.testTrick, 0)
        self.assertEqual(len(self.testTrick.get_played_cards_list()), 2)
        self.assertEqual(self.testTrick.get_suit_lead(), "hearts")
        self.assertEqual(self.testTrick.get_winning_player(), self.tempPlayers[0])
        self.tempPlayers[2].accept(Card(0, "trump"))
        self.tempPlayers[2].get_hand().play_card_at_index(self.testTrick, 0)
        self.assertEqual(self.testTrick.get_winning_player(), self.tempPlayers[2])

    def test_on_fill(self):
        for i in range(4):
            self.tempPlayers[i].get_hand().play_card_at_index(self.testTrick, 0)
        self.assertEqual(self.testTrick.get_winning_card(), Card(-1, "null"))

    def tearDown(self):
        self.testTrick._winning_card = Card(-1, "null")
        self.testTrick._played_cards_list = [None, None, None, None]
        for player in self.tempPlayers:
            del player
        del self.tempPlayers
        del self.testTrick

if __name__ == "__main__":
    unittest.main()