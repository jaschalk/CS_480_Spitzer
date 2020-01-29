import unittest
import Deck

class TestDeck(unittest.TestCase):
    
    def setUp(self):
        self.deck = Deck

    def test_default_deck(self):
        self.assertEqual(self.deck.cardList.size(), 32)
    
    def test_deck_dealing(self):
        self.tempPlayer = Player
        startSize = self.deck.cardList.size()
        self.deck.deal(self.tempPlayer)
        self.assertEqual(startSize, self.deck.cardList.size() - 8)
        del self.tempPlayer

    def tearDown(self):
        del self.deck
