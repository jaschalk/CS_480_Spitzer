import unittest
from GameObjects import *

class RoundTest(unittest.TestCase):

    def setUp(self):
        self.tempPlayers = []
        for i in range(4):
            self.tempPlayers.append(Player())
        self.testRound = Round(self.tempPlayers)

    def test_init(self):
        self.assertIsInstance(self.testRound.currentTrick, Trick)
        self.assertEqual(self.testRound.trickHistory.size(),4)
        self.assertEqual(self.testRound.trickHistory[0].size(),8)
        self.assertEqual(self.testRound.trickHistory[0][0].size(),32)
        #32 cards in order: QC,7D,QS,QH,QD,JC,JS,JH,JD,AD,10D,KD,9D,8D,(A,10,K,9,8,7)C,(A,10,K,9,8,7)S,(A,10,K,9,8,7)H
        self.assertEqual(self.testRound.playerList.size(), 4)
        self.assertEqual(self.testRound.partnersMatrix.size(), 4) #4x4 for each players relation to all other players
        self.assertEqual(self.testRound.partnersMatrix[0].size(), 4)
        self.assertEqual(self.testRound.callMatrix.size(), 4)
        self.assertEqual(self.testRound.callMatrix[0].size(), 6) #4x6 for each players call state of: 3 ace calls, and 3 solo calls
        for row in range(4):
            for col in range(6):
                self.assertEqual(self.testRound.callMatrix[row][col], 0)

    def test_on_trick_finish(self):
        self.tempTrick = Trick(self.testRound, self.tempPlayers[0])
        for i in range(4):
            self.tempPlayers[i].accept(FailCard(12-i, "Clubs"))
            self.tempPlayers[i].playValidCard(self.tempTrick)
        #Now the trick should be finished and we can test accordingly
        for i in range(4):
            self.assertEqual(self.testRound.trickHistory[i][0][12-i], 1)
            #The 3rd player will have played the Ace of Clubs, the 2nd player the 10 of Clubs, the 1st the King of Clubs, the 0th the 9 of Clubs
        self.assertEqual(self.testRound.leadingPlayer, self.tempPlayers[3])
        
    
    def test_on_round_finish(self):
        #Need to use a method to run a round to completion here, not manually step through
        self.tempDeck = Deck()
        for player in self.tempPlayers:
            self.tempDeck.deal_cards_to(player)
        #On Round finish: 


    def tearDown(self):
        for player in self.tempPlayers:
            del player
        del self.tempPlayers
        del self.testRound

if __name__ == "__main__":
    unittest.main()