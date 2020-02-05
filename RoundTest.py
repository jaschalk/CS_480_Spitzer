import unittest
from GameObjects import *

class RoundTest(unittest.TestCase):

    def setUp(self):
        self.tempPlayers = []
<<<<<<< HEAD
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
        
=======
        for i in range(4):
            self.tempPlayers.append(Player())
            self.tempPlayers[i].accept(FailCard(9+i, "spades"))
        self.testRound = Round(self.tempPlayers)

    def test_init(self):
        self.assertIsInstance(self.testRound.currentTrick, Trick)
        self.assertEqual(self.testRound.trickHistory.size(),4)
        self.assertEqual(self.testRound.trickHistory[0].size(),8)
        self.assertEqual(self.testRound.trickHistory[0][0].size(),32)
        self.assertEqual(self.testRound.playerList.size(), 4)
        self.assertEqual(self.testRound.partnersMatrix.size(), 4) #4x4 for each players relation to all other players
        self.assertEqual(self.testRound.partnersMatrix[0].size(), 4)
        self.assertEqual(self.testRound.callMatrix.size(), 4)
        self.assertEqual(self.testRound.callMatrix[0].size(), 6) #4x6 for each players call state of: 3 ace calls, and 3 solo calls
        for row in range(4):
            for col in range(6):
                self.assertEqual(self.testRound.callMatrix[row][col], 0)
    
    def test_on_round_finish(self):
        self.tempPlayers[0].playValidCard() #should this use structural recursion to progress play?

    def tearDown(self):
        for player in self.tempPlayers:
            del player
        del self.tempPlayers
        del self.testRound

>>>>>>> dev
if __name__ == "__main__":
    unittest.main()