import unittest
from GameObjects import *

class TrickTest(unittest.TestCase):

    def setUp(self):
        self.testTrick = Trick(None, None)

    def test_on_init(self):
        self.assertEqual(self.testTrick.cardsInPlay.size(), 0)
        self.tempCard1 = FailCard(12,"hearts")
        self.testTrick.accept(self.tempCard1)
        self.assertEqual(self.testTrick.cardsInPlay.size(), 1)
        self.tempCard2 = FailCard(11,"hearts")

    def test_on_fill(self):
        self.tempPlayers = []
        for i in range(4):
            self.tempPlayers.append(Player(i))
            self.tempPlayers[i].accept(FailCard(9+i, "hearts"))
            self.testTrick.accept(self.tempPlayers[i].cards[0])


    def tearDown(self):
        del self.testTrick

if __name__ == "__main__":
    unittest.main()