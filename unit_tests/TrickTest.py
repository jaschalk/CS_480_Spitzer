import unittest
from game_objects.Trick import Trick
from game_objects.Player import Player
from game_objects.Card import Card
from game_objects.Round import Round

class TrickTest(unittest.TestCase):

    def setUp(self):
        self.testTrick = Trick(None, None)
        self.testTrick.parentRound = Round(0)
        self.tempPlayers = []
        for i in range(4):
            self.tempPlayers.append(Player(None, i, None))
        self.testTrick.parentRound.playerList = self.tempPlayers
        for i in range(4):
            self.tempPlayers[i].accept(Card(9+i, "hearts"))

    def test_on_init(self):
        self.assertEqual(len(self.testTrick.get_played_cards_list()), 0)
        self.assertIsNone(self.testTrick.get_suit_lead())
        self.assertIsNone(self.testTrick.get_parent_round())
        self.assertIsNone(self.testTrick.get_leading_player())
        self.assertIsNone(self.testTrick.get_winning_player)
        self.assertEqual(self.testTrick.get_points_on_trick(), 0)

    def test_on_accept_card(self):
        self.testTrick.accept(self.tempPlayers[0].hand.play_card(0))
        self.assertEqual(len(self.testTrick.get_played_cards_list()), 1)
        self.assertEqual(self.testTrick.get_suit_lead(), "hearts")
        self.assertEqual(self.testTrick.get_winning_player(), self.tempPlayers[0])
        self.testTrick.accept(self.tempPlayers[1].hand.play_card(0))
        self.assertEqual(len(self.testTrick.get_played_cards_list()), 2)
        self.assertEqual(self.testTrick.get_suit_lead(), "hearts")
        self.assertEqual(self.testTrick.get_winning_player(), self.tempPlayers[0])
        self.tempPlayers[2].accept(Card(0, "trump"))
        self.testTrick.accept(self.tempPlayers[2].hand.play_card(1))
        self.assertEqual(self.testTrick.get_winning_player(), self.tempPlayers[2])

    def test_on_fill(self):
        for i in range(4):
            self.testTrick.accept(self.tempPlayers[i].hand.cards[0])
        self.assertIsNone(self.testTrick)

    def tearDown(self):
        for player in self.tempPlayers:
            del player
        del self.tempPlayers
        del self.testTrick.parentRound
        del self.testTrick

if __name__ == "__main__":
    unittest.main()