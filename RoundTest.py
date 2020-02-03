import unittest
from GameObjects import *

class RoundTest(unittest.TestCase):

    def setUp(self):
        self.tempPlayers = []
        self.tempGame = Game()
        for i in range(4):
            self.tempPlayers.append(Player(i))
        self.testRound = Round(self.tempPlayers)
        self.testRound.parentGame = self.tempGame

    def test_init_case(self):
        self.assertIsInstance(self.testRound.currentTrick, Trick)


    def tearDown(self):
        del self.testRound
        del self.tempPlayers
        del self.tempGame
        
if __name__ == "__main__":
    unittest.main()