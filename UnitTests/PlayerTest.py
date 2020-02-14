import unittest
from GameObjects import *

class PlayerTest(unittest.TestCase):

    def setUp(self):
       self.testPlayer = Player(0)
       self.tempPlayers = []
       self.tempPlayers[0] = self.testPlayer
       for index in range(1,4):
           self.tempPlayers[index] = Player(index)

    def test_on_init(self):
        self.assertEqual(self.testPlayer.roundScore, 0)
        self.assertEqual(self.testPlayer.totalScore, 0)
        self.assertFalse(self.testPlayer.isLeading)
        self.assertIsInstance(self.testPlayer.hand, Hand)
        self.assertIsInstance(self.testPlayer.validCallsList.size(), 8)
        self.assertEqual(self.testPlayer.potentialPartnersList.size(), 4)
        self.assertEqual(self.testPlayer.potentialPartnersList[0], 1)
        for index in range(1,4):
            self.assertAlmostEqual(self.testPlayer.potentialPartnersList[index], 1/3)

    def test_trick_complete(self):
        testRound = Round(self.tempPlayers)
        testTrick = Trick(testRound)
        testRound.currentTrick = testTrick
        currentRoundScore = self.testPlayer.roundScore
        for index in range(4):
            self.tempPlayers[index].accept(Card(index, "trump"))
            self.tempPlayers[index].playValidCard(testTrick)
        self.assertEqual(self.testPlayer.roundScore, 9)
        self.assertEqual(self.testPlayer.roundScore, (currentRoundScore + self.testPlayer.trickScore))
        self.assertEqual(self.tempPlayers[0].potentialPartnersList, [1,0,1,0])
        self.assertEqual(self.tempPlayers[1].potentialPartnersList, [0,1,0,1])
        self.assertEqual(self.tempPlayers[2].potentialPartnersList, [1,0,1,0])
        self.assertEqual(self.tempPlayers[3].potentialPartnersList, [0,1,0,1])

    def test_card_acceptance(self):
        for index in range(5):
            self.testPlayer.accept(Card(index, "trump"))
        self.assertEqual(self.testPlayer.hand.cardsInHand[5], Card(5, "trump"))
    
    #Create a test to test a method calling upon the tree to modify the Players' potential partners lists.
    def test_no_call_is_made(self):
        self.testPlayer.makeCall(0)
        self.assertEqual(self.testPlayer.potentialPartnersList[0], 1)
        for index in range(1,4):
            self.assertAlmostEqual(self.testPlayer.potentialPartnersList[index], 1/3)

    def tearDown(self):
        for index in range(4):
            del self.tempPlayers[index]
        del self.tempPlayers

if __name__ == "__main__":
    unittest.main()