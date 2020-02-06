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
            self.tempPlayers[index].accept(TrumpCard(index))
        for index in range(4):
            self.tempPlayers[index].playValidCard(testTrick)
        self.assertEqual(self.testPlayer.roundScore, (currentRoundScore + self.testPlayer.trickScore))
        self.assertEqual(self.tempPlayers[0].potentialPartnersList, [1,0,1,0])
        self.assertEqual(self.tempPlayers[1].potentialPartnersList, [0,1,0,1])
        self.assertEqual(self.tempPlayers[2].potentialPartnersList, [1,0,1,0])
        self.assertEqual(self.tempPlayers[3].potentialPartnersList, [0,1,0,1])

    #When testing for ace calls, and first trick calls give cards to all players and update all the ppl based on
    #the call made and who has what cards
    #When testing for first trick give cards to players in a way that I know who will win the trick, assert that that
    #all ppl are updated according to who won the trick.
    #Look in round to find list of cards in order of rank and an example of playing out a trick.
    
    def test_zss_call_is_made(self):
        self.testPlayer.makeCall(7)
        self.assertEqual(self.testPlayer.potentialPartnersList, [1,0,0,0])

    def test_zss_call_is_made(self):
        self.testPlayer.makeCall(7)
        self.assertEqual(self.testPlayer.potentialPartnersList, [1,0,0,0])

    def test_zss_call_is_made(self):
        self.testPlayer.makeCall(7)
        self.assertEqual(self.testPlayer.potentialPartnersList, [1,0,0,0])

    def test_zss_call_is_made(self):
        self.testPlayer.makeCall(7)
        self.assertEqual(self.testPlayer.potentialPartnersList, [1,0,0,0])

    def test_zss_call_is_made(self):
        self.testPlayer.makeCall(7)
        self.assertEqual(self.testPlayer.potentialPartnersList, [1,0,0,0])

    def test_zss_call_is_made(self):
        self.testPlayer.makeCall(7)
        self.assertEqual(self.testPlayer.potentialPartnersList, [1,0,0,0])

    def test_zss_call_is_made(self):
        self.testPlayer.makeCall(7)
        self.assertEqual(self.testPlayer.potentialPartnersList, [1,0,0,0])

    def test_zss_call_is_made(self):
        self.testPlayer.makeCall(7)
        self.assertEqual(self.testPlayer.potentialPartnersList, [1,0,0,0])

    #When testing for mid trick update, give each player a known set of cards such that when a card is played
    #we know what the new list should be 

if __name__ == "__main__":
    unittest.main()