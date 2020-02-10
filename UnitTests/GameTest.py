import unittest
from GameObjects import *

class GameTest(unittest.TestCase):

    def setUp(self):
        self.testGame = Game()
        self.tempPlayer1 = Player()
        self.tempPlayer2 = Player()
        self.tempPlayer3 = Player()
        self.tempPlayer4 = Player()

    def test_on_init(self):
        self.assertEqual(self.testGame.listOfPlayers.size(), 4)
        self.assertIsInstance(self.testGame.deck, Deck)
        self.assertEqual(self.testGame.listOfRounds.size(), 0)
        self.assertIsInstance(self.testGame.cardRules, CardRules)
        self.assertIsInstance(self.testGame.partnerRules, PartnerRules)
        self.assertIsInstance(self.testGame.callRules, CallRules)

    def test_deal_cards(self):
        tempPlayer = Player()
        self.testGame.deal_cards_to(tempPlayer)
        self.assertEqual((self.testGame.deck + tempPlayer.hand.size()), 32)

    def test_end_game_one_winner(self):
        self.tempPlayer1.totalScore = 42
        self.tempPlayer2.totalScore = 30
        self.tempPlayer3.totalScore = 28
        self.tempPlayer4.totalScore = 20
        self.assertTrue(self.tempPlayer1.wins()) #Have this method return a boolean on whether or not the asking player wins.

    def test_end_game_tie(self):
        self.tempPlayer1.totalScore = 42
        self.tempPlayer2.totalScore = 42
        self.tempPlayer3.totalScore = 28
        self.tempPlayer4.totalScore = 20
        self.assertTrue(self.tempPlayer1.tie(self.tempPlayer2)) #Have this method return a boolean on whether or not the asking player ties with the argument player
        #test if new round is created?

    def test_end_game_continues(self):
        self.tempPlayer1.totalScore = 36
        self.tempPlayer2.totalScore = 30
        self.tempPlayer3.totalScore = 28
        self.tempPlayer4.totalScore = 20
        #test if new round is created?

    if __name__ == "__main__":
        unittest.main()