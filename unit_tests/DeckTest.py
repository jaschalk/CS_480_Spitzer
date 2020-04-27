import unittest
from game_objects.Deck  import Deck
from game_objects.Player import Player

class TestDeck(unittest.TestCase):
    
    def setUp(self):
        self.testDeck = Deck()

    def test_default_deck(self):
        self.assertEqual(len(self.testDeck.get_card_list()), 32)
    
    def test_deck_dealing(self):
        self.tempPlayer = Player(None, 0, None)
        startSize = len(self.testDeck.get_card_list())
        self.testDeck.deal_cards_to(self.tempPlayer)
        self.assertEqual(startSize, len(self.testDeck.get_card_list()) + 8)
        del self.tempPlayer

    def tearDown(self):
        del self.testDeck

if __name__ == "__main__":
    unittest.main()