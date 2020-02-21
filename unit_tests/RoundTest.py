import unittest
import copy
import pickle
from GameObjects import *

class RoundTest(unittest.TestCase):

    def setUp(self):
        self.tempPlayers = []
        for i in range(4):
            self.tempPlayers.append(Player(i))
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
        self.assertEqual(self.testRound.callMatrix[0].size(), 8) #4x8 for each players call state of: no call, first trick, AC call, AS call, AH call, and 3 solo calls
        for row in range(4):
            for col in range(8):
                if col == 0:
                    self.assertEqual(self.testRound.callMatrix[row][col], 1)
                else:
                    self.assertEqual(self.testRound.callMatrix[row][col], 0)

    def test_on_trick_finish(self):
        tempTrick = Trick(self.testRound, self.tempPlayers[0])
        initial_card_count = 0
        for i in range(4):
            self.tempPlayers[i].accept(Card(12-i, "clubs"))
            initial_card_count += self.tempPlayers[i].hand.cardList.size()
        for i in range(4):
            self.tempPlayers[i].playValidCard(tempTrick)
        post_trick_card_count = 0
        for i in range(4):
            post_trick_card_count += self.tempPlayers[i].hand.cardList.size()
        self.assertEqual(initial_card_count, post_trick_card_count+4)
        #Now the trick should be finished and we can test accordingly
        tempPlayerTrickScore = copy.copy(self.tempPlayers[3].trickScore)
        for i in range(4):
            self.assertEqual(self.testRound.trickHistory[i][0][12-i], 1)
            #The 3rd player will have played the Ace of Clubs, the 2nd player the 10 of Clubs, the 1st the King of Clubs, the 0th the 9 of Clubs
        self.assertEqual(self.testRound.leadingPlayer, self.tempPlayers[3])
        self.assertEqual(self.testRound.point_history[3][0], 25)#Check if the Trick Point history has updated properly


    def test_potential_partners_history(self): #Check if the Potential Partners history has been updated properly
        tempTrick = Trick(self.testRound, self.tempPlayers[0])
        for i in range(4):
            self.tempPlayers[i].accept(Card(i, "trump")) # (P0, QC), (P1, 7D), (P2, QS), (P3, QH)
            self.tempPlayers[i].playValidCard(tempTrick)
        #               self.testRound.potential_partners_history[player_num][potential_partner_num][trick_depth]
        self.assertEqual(self.testRound.potential_partners_history[0][2][0], 1)
        self.assertEqual(self.testRound.potential_partners_history[1][3][0], 1)
        self.assertEqual(self.testRound.potential_partners_history[2][0][0], 1)
        self.assertEqual(self.testRound.potential_partners_history[3][1][0], 1)
        
    def test_on_round_finish(self):
        tempGame = Game()
        tempDeck = Deck()
        tempGame.deck = tempDeck
        initialPlayerScores = []
        tempGame.playerList = self.tempPlayers
        for player in self.tempPlayers:
            tempDeck.deal_cards_to(player)
            initialPlayerScores.append(player.roundScore)
        #On Round finish:
        #tell players to update total scores, tell the game to repopulate the deck, if the game has not ended (make a new deck)
        self.testRound.playRound() #Need to use a method to run a round to completion here, not manually step through
        self.assertNotEqual(sum(self.testRound.scoreList), 0) #after a round has been played the sum of the scores cannot be 0
        self.assertEqual(tempDeck.cardList.size(), 32)
        
    def test_file_out_behavior(self):
        tempDeck = Deck()
        for player in self.tempPlayers:
            tempDeck.deal_cards_to(player)
        self.testRound.playRound()
        #have some sort of file out happen. Assert that the data read back in from the file equals the data that was stored
        with open(self.testRound.file_name, 'rb') as input:
            file_data = pickle.load(input)
            self.assertEqual(self.testRound.file_data, file_data)

    def tearDown(self):
        for player in self.tempPlayers:
            del player
        del self.tempPlayers
        del self.testRound

if __name__ == "__main__":
    unittest.main()