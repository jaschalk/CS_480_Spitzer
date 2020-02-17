import unittest
from GameObjects import PartnerRuleTree as PRT
from GameObjects import Player
from GameObjects import Round
from GameObjects import Trick
from GameObjects import Card

class PartnerRuleTest(unittest.TestCase):

    def setUp(self):
        self.testTree = PRT.PartnerRuleTree()
        self.tempRound = Round.Round(0)
        self.tempTrick = Trick.Trick(self.tempRound, None)
        self.tempRound.currentTrick = self.tempTrick
        self.tempPlayerList = []
        for index in range(4):
            self.tempPlayerList.append(Player.Player(index))
        self.cardList = []
        for index in range(14):
            self.cardList.append(Card.Card(index, "trump"))
        for index in range(9,15):
            self.cardList.append(Card.Card(index, "clubs"))
        for index in range(9,15):
            self.cardList.append(Card.Card(index, "spades"))
        for index in range(9,15):
            self.cardList.append(Card.Card(index, "hearts"))
    
    def test_first_trick_called(self):
        for index in range(5):
            self.tempPlayerList[0].accept(self.cardList[index]) #give the first player the first 5 trump cards (includes both queens)
        self.tempPlayerList[0].accept(self.cardList[14]) #give the first player all 3 fail aces
        self.tempPlayerList[0].accept(self.cardList[20])
        self.tempPlayerList[0].accept(self.cardList[26])
        for index in range(5, 13):
            self.tempPlayerList[1].accept(self.cardList[index]) #give the second player the next 8 trump cards
        for index in range(13, 23):
            if index != 14:
                if index != 20:
                    self.tempPlayerList[2].accept(self.cardList[index]) #give the third player the next 8 cards, skipping any aces
                else:
                    continue
        for index in range(23, 32):
            if index != 26:
                self.tempPlayerList[3].accept(self.cardList[index]) #give the fourth player the last 8 cards, skipping any aces
            else:
                continue
        self.tempPlayerList[0].makeCall(4)
        self.tempPlayerList[0].hand.playCard(20, self.tempTrick) #AS
        self.tempPlayerList[1].hand.playCard(13, self.tempTrick) #8D player 2 wins the trick
        self.tempPlayerList[2].hand.playCard(22, self.tempTrick) #KS
        self.tempPlayerList[3].hand.playCard(23, self.tempTrick) #9S
        self.assertEqual(self.tempPlayerList[0].potentialPartnersList, [1,1,0,0])
        self.assertEqual(self.tempPlayerList[1].potentialPartnersList, [1,1,0,0])
        self.assertEqual(self.tempPlayerList[1].potentialPartnersList, [0,0,1,1])
        
    def test_ace_called(self):
        self.tempPlayerList[0].accept(self.cardList[0]) #give player 1 both black queens and 7, 8, 9 of spades and hearts
        self.tempPlayerList[0].accept(self.cardList[2])
        for index in range(12, 15):
            self.tempPlayerList[0].accept(Card.Card(index, "spades"))
            self.tempPlayerList[0].accept(Card.Card(index, "hearts"))
        for index in range(9, 11):
            self.tempPlayerList[1].accept(Card.Card(index, "trump")) #give player 2 all aces and 10s
            self.tempPlayerList[1].accept(Card.Card(index, "clubs"))
            self.tempPlayerList[1].accept(Card.Card(index, "spades"))
            self.tempPlayerList[1].accept(Card.Card(index, "hearts"))
        for index in range(3, 9):
            self.tempPlayerList[2].accept(Card.Card(index, "trump")) #give player 3 a bunch of random trump cards
        self.tempPlayerList[2].accept(self.cardList[1]) #spitzer
        self.tempPlayerList[2].accept(self.cardList[11]) #KD
        self.tempPlayerList[0].makeCall(3)
        self.assertEqual(self.tempPlayerList[1].potentialPartnersList, [1,1,0,0]) #Only update the potential partners list of the player with the ace matching the one called.
        self.assertEqual(self.tempPlayerList[0].potentialPartnersList[0], 1)
        for index in range(1,4):
            self.assertAlmostEqual(self.tempPlayerList[0].potentialPartnersList[index], 1/3)

    def test_solo_called(self):
        self.tempPlayerList[0].makeCall(5)
        self.assertEqual(self.tempPlayerList[0].potentialPartnersList, [1,0,0,0])
        self.assertEqual(self.tempPlayerList[1].potentialPartnersList, [0,1,1,1])
        self.assertEqual(self.tempPlayerList[2].potentialPartnersList, [0,1,1,1])
        self.assertEqual(self.tempPlayerList[3].potentialPartnersList, [0,1,1,1])

    def test_no_call_both_queens(self):
        for index in range(8):
            self.tempPlayerList[0].accept(self.cardList[index]) #Give player 1 the first 8 cards
        self.assertEqual(self.tempPlayerList[0].potentialPartnersList, [1,0,0,0])

    def test_no_call_one_queen_played(self):
        self.tempPlayerList[0].accept(self.cardList[0])
        self.tempPlayerList[1].accept(self.cardList[2])
        self.tempPlayerList[1].accept(self.cardList[1])
        self.tempPlayerList[2].accept(self.cardList[30])
        self.tempPlayerList[3].accept(self.cardList[31])
        self.tempPlayerList[0].hand.playCard(0, self.tempTrick) 
        self.tempPlayerList[1].hand.playCard(1, self.tempTrick)
        self.tempPlayerList[2].hand.playCard(30, self.tempTrick)
        self.tempPlayerList[3].hand.playCard(31, self.tempTrick)
        self.assertEqual(self.tempPlayerList[0].potentialPartnersList[0], 1)
        for index in range(1,4):
            self.assertAlmostEqual(self.tempPlayerList[0].potentialPartnersList[index], 1/3)
        self.assertEqual(self.tempPlayerList[1].potentialPartnersList, [1,1,0,0])
        self.assertEqual(self.tempPlayerList[2].potentialPartnersList[0], 0)
        self.assertAlmostEqual(self.tempPlayerList[2].potentialPartnersList[1], 1/2)
        self.assertEqual(self.tempPlayerList[2].potentialPartnersList[2], 1)
        self.assertAlmostEqual(self.tempPlayerList[2].potentialPartnersList[3], 1/2)
        self.assertEqual(self.tempPlayerList[3].potentialPartnersList[0], 0)
        self.assertAlmostEqual(self.tempPlayerList[3].potentialPartnersList[1], 1/2)
        self.assertAlmostEqual(self.tempPlayerList[3].potentialPartnersList[2], 1/2)
        self.assertEqual(self.tempPlayerList[3].potentialPartnersList[3], 1)
        
    def test_no_call_no_queen_played(self):
        self.tempPlayerList[0].accept(self.cardList[0])
        self.tempPlayerList[0].accept(self.cardList[3])
        self.tempPlayerList[1].accept(self.cardList[2])
        self.tempPlayerList[1].accept(self.cardList[1])
        self.tempPlayerList[2].accept(self.cardList[30])
        self.tempPlayerList[2].accept(self.cardList[29])
        self.tempPlayerList[3].accept(self.cardList[31])
        self.tempPlayerList[3].accept(self.cardList[28])
        self.tempPlayerList[0].hand.playCard(3, self.tempTrick) 
        self.tempPlayerList[1].hand.playCard(1, self.tempTrick)
        self.tempPlayerList[2].hand.playCard(30, self.tempTrick)
        self.tempPlayerList[3].hand.playCard(31, self.tempTrick)
        for index in range(4):
            self.assertEqual(self.tempPlayerList[index].potentialPartnersList[index], 1)
            for i in range(4):
                self.assertAlmostEqual(self.tempPlayerList[index].potentialPartnersList[i], 1/3)

if __name__ == "__main__":
    unittest.main()