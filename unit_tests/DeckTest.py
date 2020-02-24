import unittest
from game_objects import *

class TestDeck(unittest.TestCase):
    
    def setUp(self):
        self.testDeck = Deck.Deck()

    def test_default_deck(self):
        self.assertEqual(self.testDeck.cardList.size(), 32)
    
    def test_deck_dealing(self):
        self.tempPlayer = Player.Player()
        startSize = self.testDeck.cardList.size()
        self.testDeck.deal_cards_to(self.tempPlayer)
        self.assertEqual(startSize, self.testDeck.cardList.size() + 8)
        del self.tempPlayer

    def tearDown(self):
        del self.testDeck

if __name__ == "__main__":
    unittest.main()