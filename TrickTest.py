import unittest
from GameObjects import *

class TrickTest(unittest.TestCase):

    def setUp(self):
        self.testTrick = Trick(None, None)
        self.testTrick.parentRound = Round(0)
        self.tempPlayers = [Player(0), Player(1), Player(2), Player(3)]
        self.testTrick.parentRound.playerList = self.tempPlayers
        for i in range(4):
            self.tempPlayers[i].accept(FailCard(10+i, "hearts"))

    def test_on_init(self):
        self.assertEqual(self.testTrick.cardsInPlay.size(), 0)
        self.assertIsNone(self.testTrick.suitLead)
        self.assertIsNone(self.testTrick.parentRound)
        self.assertIsNone(self.testTrick.leadingPlayer)
        self.assertIsNone(self.testTrick.winnningPlayer)
        self.assertEqual(self.testTrick.containedPoints, 0)

    def test_on_accept_card(self):
        self.testTrick.accept(self.tempPlayers[0].hand.play_card(0))
        self.assertEqual(self.testTrick.playedCards.size(), 1)
        self.assertEqual(self.testTrick.suitlead, "hearts")
        self.assertEqual(self.testTrick.winningPlayer, self.tempPlayers[0])
        self.testTrick.accept(self.tempPlayers[1].hand.play_card(0))
        self.assertEqual(self.testTrick.playedCards.size(), 2)
        self.assertEqual(self.testTrick.suitlead, "hearts")
        self.assertEqual(self.testTrick.winningPlayer, self.tempPlayers[0])
        self.tempPlayers[2].accept(TrumpCard(0))
        self.testTrick.accept(self.tempPlayers[2].hand.play_card(1))
        self.assertEqual(self.testTrick.winningPlayer, self.tempPlayers[2])

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