import unittest
import Deck

class TestDeck(unittest.TestCase):
    
    def setUp(self):
        self.deck = Deck

    def test_default_deck(self):
        self.assertEqual(self.deck.cardList.size(), 32)
        startSize = self.deck.cardList.size()
        self.tempPlayer = Player
        self.deck.deal(self.tempPlayer)
        self.assertEqual(startSize, self.deck.cardList.size() - 8)