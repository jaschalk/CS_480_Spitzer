import unittest
from game_objects import *

class HandTest(unittest.TestCase):

    def setUp(self):
        self.testHand = Hand()

    def test_on_init(self):
        self.assertEqual(self.testHand.cardsInHand.size(), 0)
        for entry in self.testHand.validPlayList:
            self.assertTrue(entry)

    def test_on_deal(self):
        self.tempDeck = Deck()
        self.tempPlayer = Player()
        self.tempPlayer.hand = self.testHand
        self.tempDeck.deal_cards_to(self.tempPlayer)
        self.assertEqual(self.testHand.cardsInHand.size(), 8)

    def test_card_played(self):
        self.tempTrick = Trick()
        startHandSize = self.testHand.cardsInHand.size()
        startValidListSize = self.testHand.validPlayList.size()
        self.testHand.playCard(self.tempTrick)
        self.assertEqual(self.testHand.cardsInHand.size(), startHandSize - 1)
        self.testHand.updateValidPlay()
        self.assertEqual(self.testHand.validPlayList.size(), startValidListSize - 1)


    def tearDown(self):
        del self.testHand

if __name__ == "__main__":
    unittest.main()