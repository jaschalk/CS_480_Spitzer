import unittest
from GameObjects import PartnerRuleTree as PRT
from GameObjects import Player
from GameObjects import Round
from GameObjects import Trick
from GameObjects import Card

#HAVE THE arePartners METHOD RETURN A BOOLEAN. TRUE = PLAYERS ARE PARTNERS. FALSE = PLAYERS ARE NOT PARTNERS OR UNSURE. (This is my initial thought)
#All of the ace calls and solo calls look almost identical. Is there a shorter way to test for any of this?????

#This is getting very long. I feel like I am caring about too many players...?
#I only used 3 players for all of the ace calls, since the fourth player is not really needed. Or is it?

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
        self.assertTrue(self.testTree.arePartners(self.tempPlayerList[0], self.tempPlayerList[1], self.tempRound)) #asking player makes call and target player wins the trick
        self.assertFalse(self.testTree.arePartners(self.tempPlayerList[0], self.tempPlayerList[2], self.tempRound)) #asking player makes call and target player doesn't win the trick
        self.assertTrue(self.testTree.arePartners(self.tempPlayerList[1], self.tempPlayerList[0], self.tempRound)) #target player makes call and asking player takes the trick
        self.assertFalse(self.testTree.arePartners(self.tempPlayerList[2], self.tempPlayerList[0], self.tempRound)) #target player makes call and asking player does not take the trick
        #do i need to test every combination of partners on this call because it is known by all players who the partners are at the end of the trick?

    def test_ace_of_hearts_called(self):
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
            self.tempPlayersList[2].accept(Card.Card(index, "trump")) #give player 3 a bunch of random trump cards
        self.tempPlayersList[2].accept(self.cardList[1]) #spitzer
        self.tempPlayersList[2].accept(self.cardList[11]) #KD
        self.tempPlayerList[0].makeCall(3)
        self.assertTrue(self.testTree.arePartners(self.tempPlayerList[0], self.tempPlayerList[1], self.tempRound)) #asking player makes call and target player has ace called
        self.assertFalse(self.testTree.arePartners(self.tempPlayerList[0], self.tempPlayerList[2], self.tempRound)) #asking player makes call and target player doesn't have ace called
        self.assertTrue(self.testTree.arePartners(self.tempPlayerList[1], self.tempPlayerList[0], self.tempRound)) #target player makes call and asking player has ace called
        self.assertFalse(self.testTree.arePartners(self.tempPlayerList[2], self.tempPlayerList[0], self.tempRound)) #target player makes call and asking player does not have ace called

    def test_ace_of_spades_called(self):
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
            self.tempPlayersList[2].accept(Card.Card(index, "trump")) #give player 3 a bunch of random trump cards
        self.tempPlayersList[2].accept(self.cardList[1]) #spitzer
        self.tempPlayersList[2].accept(self.cardList[11]) #KD
        self.tempPlayerList[0].makeCall(2)
        self.assertTrue(self.testTree.arePartners(self.tempPlayerList[0], self.tempPlayerList[1], self.tempRound)) #asking player makes call and target player has ace called
        self.assertFalse(self.testTree.arePartners(self.tempPlayerList[0], self.tempPlayerList[2], self.tempRound)) #asking player makes call and target player doesn't have ace called
        self.assertTrue(self.testTree.arePartners(self.tempPlayerList[1], self.tempPlayerList[0], self.tempRound)) #target player makes call and asking player has ace called
        self.assertFalse(self.testTree.arePartners(self.tempPlayerList[2], self.tempPlayerList[0], self.tempRound)) #target player makes call and asking player does not have ace called

    def test_ace_of_clubs_called(self):
        self.tempPlayerList[0].accept(self.cardList[0]) #give player 1 both black queens and 7, 8, 9 of clubs and hearts
        self.tempPlayerList[0].accept(self.cardList[2])
        for index in range(12, 15):
            self.tempPlayerList[0].accept(Card.Card(index, "clubs"))
            self.tempPlayerList[0].accept(Card.Card(index, "hearts"))
        for index in range(9, 11):
            self.tempPlayerList[1].accept(Card.Card(index, "trump")) #give player 2 all aces and 10s
            self.tempPlayerList[1].accept(Card.Card(index, "clubs"))
            self.tempPlayerList[1].accept(Card.Card(index, "spades"))
            self.tempPlayerList[1].accept(Card.Card(index, "hearts"))
        for index in range(3, 9):
            self.tempPlayersList[2].accept(Card.Card(index, "trump")) #give player 3 a bunch of random trump cards
        self.tempPlayersList[2].accept(self.cardList[1]) #spitzer
        self.tempPlayersList[2].accept(self.cardList[11]) #KD
        self.tempPlayerList[0].makeCall(1)
        self.assertTrue(self.testTree.arePartners(self.tempPlayerList[0], self.tempPlayerList[1], self.tempRound)) #asking player makes call and target player has ace called
        self.assertFalse(self.testTree.arePartners(self.tempPlayerList[0], self.tempPlayerList[2], self.tempRound)) #asking player makes call and target player doesn't have ace called
        self.assertTrue(self.testTree.arePartners(self.tempPlayerList[1], self.tempPlayerList[0], self.tempRound)) #target player makes call and asking player has ace called
        self.assertFalse(self.testTree.arePartners(self.tempPlayerList[2], self.tempPlayerList[0], self.tempRound)) #target player makes call and asking player does not have ace called

    def test_z_called(self):
        for index in range(8):
            self.tempPlayers[0].accept(self.cardList[index]) #give cards to players in order
        for index in range(8, 16):
            self.tempPlayers[1].accept(self.cardList[index])
        for index in range(16, 24):
            self.tempPlayers[2].accept(self.cardList[index])
        for index in range(24, 32):
            self.tempPlayers[0].accept(self.cardList[index])
        self.tempPlayers[0].makeCall(5)
        self.assertFalse(self.testTree.arePartners(self.tempPlayerList[0], self.tempPlayerList[1], self.tempRound)) #asking player makes call
        self.assertFalse(self.testTree.arePartners(self.tempPlayerList[0], self.tempPlayerList[2], self.tempRound)) #asking player makes call
        self.assertFalse(self.testTree.arePartners(self.tempPlayerList[0], self.tempPlayerList[3], self.tempRound)) #asking player makes call
        self.assertFalse(self.testTree.arePartners(self.tempPlayerList[1], self.tempPlayerList[0], self.tempRound)) #target player makes call
        self.assertFalse(self.testTree.arePartners(self.tempPlayerList[2], self.tempPlayerList[0], self.tempRound)) #target player makes call
        self.assertFalse(self.testTree.arePartners(self.tempPlayerList[3], self.tempPlayerList[0], self.tempRound)) #target player makes call

    def test_zs_called(self):
        for index in range(8):
            self.tempPlayers[0].accept(self.cardList[index]) #give cards to players in order
        for index in range(8, 16):
            self.tempPlayers[1].accept(self.cardList[index])
        for index in range(16, 24):
            self.tempPlayers[2].accept(self.cardList[index])
        for index in range(24, 32):
            self.tempPlayers[0].accept(self.cardList[index])
        self.tempPlayers[0].makeCall(6)
        self.assertFalse(self.testTree.arePartners(self.tempPlayerList[0], self.tempPlayerList[1], self.tempRound)) #asking player makes call
        self.assertFalse(self.testTree.arePartners(self.tempPlayerList[0], self.tempPlayerList[2], self.tempRound)) #asking player makes call
        self.assertFalse(self.testTree.arePartners(self.tempPlayerList[0], self.tempPlayerList[3], self.tempRound)) #asking player makes call
        self.assertFalse(self.testTree.arePartners(self.tempPlayerList[1], self.tempPlayerList[0], self.tempRound)) #target player makes call
        self.assertFalse(self.testTree.arePartners(self.tempPlayerList[2], self.tempPlayerList[0], self.tempRound)) #target player makes call
        self.assertFalse(self.testTree.arePartners(self.tempPlayerList[3], self.tempPlayerList[0], self.tempRound)) #target player makes call

    def test_zss_called(self):
        for index in range(8):
            self.tempPlayers[0].accept(self.cardList[index]) #give cards to players in order
        for index in range(8, 16):
            self.tempPlayers[1].accept(self.cardList[index])
        for index in range(16, 24):
            self.tempPlayers[2].accept(self.cardList[index])
        for index in range(24, 32):
            self.tempPlayers[0].accept(self.cardList[index])
        self.tempPlayers[0].makeCall(7)
        self.assertFalse(self.testTree.arePartners(self.tempPlayerList[0], self.tempPlayerList[1], self.tempRound)) #asking player makes call
        self.assertFalse(self.testTree.arePartners(self.tempPlayerList[0], self.tempPlayerList[2], self.tempRound)) #asking player makes call
        self.assertFalse(self.testTree.arePartners(self.tempPlayerList[0], self.tempPlayerList[3], self.tempRound)) #asking player makes call
        self.assertFalse(self.testTree.arePartners(self.tempPlayerList[1], self.tempPlayerList[0], self.tempRound)) #target player makes call
        self.assertFalse(self.testTree.arePartners(self.tempPlayerList[2], self.tempPlayerList[0], self.tempRound)) #target player makes call
        self.assertFalse(self.testTree.arePartners(self.tempPlayerList[3], self.tempPlayerList[0], self.tempRound)) #target player makes call

if __name__ == "__main__":
    unittest.main()