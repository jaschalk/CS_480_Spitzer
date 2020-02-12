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
    
    def test_z_call_is_made(self):
        self.testPlayer.makeCall(5)
        self.assertEqual(self.testPlayer.potentialPartnersList, [1,0,0,0])

    def test_zs_call_is_made(self):
        self.testPlayer.makeCall(6)
        self.assertEqual(self.testPlayer.potentialPartnersList, [1,0,0,0])

    def test_zss_call_is_made(self):
        self.testPlayer.makeCall(7)
        self.assertEqual(self.testPlayer.potentialPartnersList, [1,0,0,0])

#32 cards in order: QC,7D,QS,QH,QD,JC,JS,JH,JD,AD,10D,KD,9D,8D,(A,10,K,9,8,7)C,(A,10,K,9,8,7)S,(A,10,K,9,8,7)H
    def test_ace_of_hearts_call_is_made(self):
        self.tempPlayers[0].hand.cardsInHand = {Card(0, "trump"), Card(2, "trump"), Card(10, "hearts"), Card(13, "hearts"), Card(11, "spades"), Card(9, "clubs"), Card(12, "hearts"), Card(14, "clubs")} #Am I doing this properly?
        self.tempPlayers[1].hand.cardsInHand = {Card(1, "trump"), Card(3, "trump"), Card(11, "hearts"), Card(14, "hearts"), Card(12, "spades"), Card(10, "clubs"), Card(9, "hearts"), Card(11, "clubs")}
        self.tempPlayers[2].hand.cardsInHand = {Card(4, "trump"), Card(6, "trump"), Card(8, "trump"), Card(10, "trump"), Card(12, "trump"), Card(12, "clubs"), Card(9, "spades"), Card(13, "spades")}
        self.tempPlayers[3].hand.cardsInHand = {Card(5, "trump"), Card(7, "trump"), Card(9, "trump"), Card(11, "trump"), Card(13, "trump"), Card(13, "clubs"), Card(10, "spades"), Card(14, "spades")}
        self.tempPlayers[0].makeCall(3)
        self.assertEqual(self.tempPlayers[1].potentialPartnersList, [1,1,0,0])

    def test_ace_of_clubs_call_is_made(self):
        self.tempPlayers[0].hand.cardsInHand = {Card(1, "trump"), Card(3, "trump"), Card(10, "hearts"), Card(13, "hearts"), Card(11, "spades"), Card(9, "clubs"), Card(12, "hearts"), Card(14, "clubs")} #Am I doing this properly?
        self.tempPlayers[1].hand.cardsInHand = {Card(0, "trump"), Card(2, "trump"), Card(11, "hearts"), Card(14, "hearts"), Card(12, "spades"), Card(10, "clubs"), Card(9, "hearts"), Card(11, "clubs")}
        self.tempPlayers[2].hand.cardsInHand = {Card(4, "trump"), Card(6, "trump"), Card(8, "trump"), Card(10, "trump"), Card(12, "trump"), Card(12, "clubs"), Card(9, "spades"), Card(13, "spades")}
        self.tempPlayers[3].hand.cardsInHand = {Card(5, "trump"), Card(7, "trump"), Card(9, "trump"), Card(11, "trump"), Card(13, "trump"), Card(13, "clubs"), Card(10, "spades"), Card(14, "spades")}
        self.tempPlayers[1].makeCall(1)
        self.assertEqual(self.tempPlayers[0].potentialPartnersList, [1,1,0,0])

    def test_ace_of_spades_call_is_made(self):
        self.tempPlayers[0].hand.cardsInHand = {Card(4, "trump"), Card(6, "trump"), Card(10, "hearts"), Card(13, "hearts"), Card(11, "spades"), Card(9, "clubs"), Card(12, "hearts"), Card(14, "clubs")} #Am I doing this properly?
        self.tempPlayers[1].hand.cardsInHand = {Card(1, "trump"), Card(3, "trump"), Card(11, "hearts"), Card(14, "hearts"), Card(12, "spades"), Card(10, "clubs"), Card(9, "hearts"), Card(11, "clubs")}
        self.tempPlayers[2].hand.cardsInHand = {Card(0, "trump"), Card(2, "trump"), Card(8, "trump"), Card(10, "trump"), Card(12, "trump"), Card(12, "clubs"), Card(9, "spades"), Card(13, "spades")}
        self.tempPlayers[3].hand.cardsInHand = {Card(5, "trump"), Card(7, "trump"), Card(9, "trump"), Card(11, "trump"), Card(13, "trump"), Card(13, "clubs"), Card(10, "spades"), Card(14, "spades")}
        self.tempPlayers[2].makeCall(2)
        self.assertEqual(self.tempPlayers[3].potentialPartnersList, [0,0,1,1])

    def test_first_trick_call_is_made(self):
        self.tempPlayers[0].hand.cardsInHand = {Card(0, "trump"), Card(2, "trump"), Card(10, "hearts"), Card(9, "hearts"), Card(9, "spades"), Card(9, "clubs"), Card(12, "hearts"), Card(14, "clubs")} #Am I doing this properly?
        self.tempPlayers[1].hand.cardsInHand = {Card(1, "trump"), Card(3, "trump"), Card(11, "hearts"), Card(14, "hearts"), Card(12, "spades"), Card(10, "clubs"), Card(13, "hearts"), Card(11, "clubs")}
        self.tempPlayers[2].hand.cardsInHand = {Card(4, "trump"), Card(6, "trump"), Card(8, "trump"), Card(10, "trump"), Card(12, "trump"), Card(12, "clubs"), Card(11, "spades"), Card(13, "spades")}
        self.tempPlayers[3].hand.cardsInHand = {Card(5, "trump"), Card(7, "trump"), Card(9, "trump"), Card(11, "trump"), Card(13, "trump"), Card(13, "clubs"), Card(10, "spades"), Card(14, "spades")}
        self.tempPlayers[0].makeCall(4)
        testRound = Round(self.tempPlayers)
        testTrick = Trick(testRound, self.tempPlayers[0])
        testRound.currentTrick = testTrick
        self.tempPlayers[0].hand.playCard(2, testTrick)        
        self.tempPlayers[1].hand.playCard(1, testTrick) #Player 2 wins the trick
        self.tempPlayers[2].hand.playCard(4, testTrick)
        self.tempPlayers[3].hand.playCard(7, testTrick)
        self.assertEqual(self.tempPlayers[0].potentialPartnersList, [1,1,0,0])
        self.assertEqual(self.tempPlayers[1].potentialPartnersList, [1,1,0,0])
        self.assertEqual(self.tempPlayers[2].potentialPartnersList, [0,0,1,1])
        self.assertEqual(self.tempPlayers[3].potentialPartnersList, [0,0,1,1])

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