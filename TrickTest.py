import unittest
from GameObjects import *

class TrickTest(unittest.TestCase):

    def setUp(self):
        self.testTrick = Trick(None, None)
        self.testTrick.parentRound = Round(0)
        self.tempPlayers = [Player(0), Player(1), Player(2), Player(3)]
        self.testTrick.parentRound.playerList = self.tempPlayers
        for i in range(4):
            self.tempPlayers[i].accept(FailCard(9+i, "hearts"))

    def test_on_init(self):
        self.assertEqual(self.testTrick.cardsInPlay.size(), 0)
        self.assertIs(self.testTrick.suitLead, None)
        self.assertIs(self.testTrick.parentRound, None)
        self.assertIs(self.testTrick.leadingPlayer, None)
        self.assertIs(self.testTrick.winnningPlayer, None)
        self.assertEqual(self.testTrick.containedPoints, 0)

    def test_on_accept_card(self):
        self.tempCard1 = FailCard(12,"hearts")
        self.testTrick.accept(self.tempCard1)
        self.assertEqual(self.testTrick.cardsInPlay.size(), 1)
        self.tempCard2 = FailCard(11,"hearts")

    def test_on_fill(self):
        for i in range(4):
            self.testTrick.accept(self.tempPlayers[i].cards[0])


    def tearDown(self):
        del self.testTrick.parentRound
        del self.testTrick

if __name__ == "__main__":
    unittest.main()