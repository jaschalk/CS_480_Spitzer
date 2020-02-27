import unittest
import copy
import numpy as np
import pickle
from game_objects.Round import Round
from game_objects.Player import Player
from game_objects.Deck import Deck
from game_objects.Trick import Trick
from game_objects.Card import Card
from game_objects.Game import Game

class RoundTest(unittest.TestCase):

    def setUp(self):
        self.tempGame = Game(0, None)
        self.tempPlayers = []
        for i in range(4):
            self.tempPlayers.append(Player(None, i, None))
        self.tempGame._players_list = self.tempPlayers
        self.testRound = Round(self.tempGame)
        
    def test_init(self):
        self.assertIsInstance(self.testRound.get_current_trick(), Trick)
        trick_history = self.testRound.get_trick_history()
        self.assertEqual(len(trick_history),4)
        self.assertEqual(len(trick_history[0]),8)
        self.assertEqual(len(trick_history[0][0]),32)
        #32 cards in order: QC,7D,QS,QH,QD,JC,JS,JH,JD,AD,10D,KD,9D,8D,(A,10,K,9,8,7)C,(A,10,K,9,8,7)S,(A,10,K,9,8,7)H
        self.assertEqual(len(self.testRound.get_players_list()), 4)
        self.assertEqual(len(self.testRound._get_player_partners()), 4) #4x4 for each players relation to all other players
        self.assertEqual(len(self.testRound._get_player_partners()[0]), 4)
        self.assertEqual(len(self.testRound.get_call_matrix()), 4)
        self.assertEqual(len(self.testRound.get_call_matrix()[0]), 8) #4x8 for each players call state of: no call, first trick, AC call, AS call, AH call, and 3 solo calls
        for row in range(4):
            for col in range(8):
                if col == 0:
                    self.assertEqual(self.testRound.get_call_matrix()[row][col], 1)
                else:
                    self.assertEqual(self.testRound.get_call_matrix()[row][col], 0)

    def test_on_trick_finish(self):
        tempTrick = Trick(self.testRound, self.tempPlayers[0])
        initial_card_count = 0
        for i in range(4):
            self.tempPlayers[i].accept(Card(12-i, "clubs"))
            initial_card_count += len(self.tempPlayers[i].hand.get_card_list())
        for i in range(4):
            self.tempPlayers[i].playValidCard(tempTrick)
        post_trick_card_count = 0
        for i in range(4):
            post_trick_card_count += len(self.tempPlayers[i].hand.cardList)
        self.assertEqual(initial_card_count, post_trick_card_count+4)
        #Now the trick should be finished and we can test accordingly
        tempPlayerTrickScore = copy.copy(self.tempPlayers[3].trickScore) # don't remember what this was for?
        for i in range(4):
            self.assertEqual(self.testRound.get_trick_history()[i][0][12-i], 1)
            #The 3rd player will have played the Ace of Clubs, the 2nd player the 10 of Clubs, the 1st the King of Clubs, the 0th the 9 of Clubs
        self.assertEqual(self.testRound.get_leading_player(), self.tempPlayers[3])
        self.assertEqual(self.testRound._get_point_history()[3][0], 25)#Check if the Trick Point history has updated properly

    def test_potential_partners_history(self): #Check if the Potential Partners history has been updated properly
        tempTrick = Trick(self.testRound, self.tempPlayers[0])
        for i in range(4):
            self.tempPlayers[i].accept(Card(i, "trump")) # (P0, QC), (P1, 7D), (P2, QS), (P3, QH)
            self.tempPlayers[i].playValidCard(tempTrick)
        #               self.testRound.potential_partners_history[player_num][potential_partner_num][trick_depth]
        self.assertEqual(self.testRound._get_potential_partners_history()[0][2][0], 1)
        self.assertEqual(self.testRound._get_potential_partners_history()[1][3][0], 1)
        self.assertEqual(self.testRound._get_potential_partners_history()[2][0][0], 1)
        self.assertEqual(self.testRound._get_potential_partners_history()[3][1][0], 1)
        
    def test_on_round_finish(self):
        tempGame = Game(0, None)
        self.testRound.set_parent_game(tempGame)
        tempDeck = Deck()
        tempGame.deck = tempDeck
        initialPlayerScores = []
        tempGame.playerList = self.tempPlayers
        for player in self.tempPlayers:
            tempDeck.deal_cards_to(player)
            initialPlayerScores.append(player.roundScore)
        #On Round finish:
        #tell players to update total scores, tell the game to repopulate the deck, if the game has not ended (make a new deck)
        self.testRound.begin_play() #Need to use a method to run a round to completion here, not manually step through
# TODO  self.assertNotEqual(sum(self.testRound.scoreList), 0) #after a round has been played the sum of the scores cannot be 0
                    # the round currently isn't storing this, I think this got moved to the game. It might be best if the the test went as well
        self.assertEqual(len(tempDeck.get_card_list()), 32)
        
    def test_file_out_behavior(self):
        tempDeck = Deck()
        for player in self.tempPlayers:
            tempDeck.deal_cards_to(player)
        self.testRound.begin_play()
        #have some sort of file out happen. Assert that the data read back in from the file equals the data that was stored
        with open(self.testRound.get_file_out_name(), 'rb') as input:
            file_data = pickle.load(input)
            self.assertEqual(self.testRound._get_file_out_data(), file_data)

    def tearDown(self):
        for player in self.tempPlayers:
            del player
        del self.tempPlayers
        del self.testRound

if __name__ == "__main__":
    unittest.main()