import unittest
from GameObjects import *

class HandTest(unittest.TestCase):

    def setUp(self):
        self.testHand = Hand() #How to fix this error

    def test_on_init(self):
        self.assertEqual(self.testHand.cardsInHand.size(), 8)
        #How to assert that a valid play list exists and is initialized to true?

    def test_card_played(self):
        startSize = self.hand.cardsInHand.size()
        self.hand.playCard() #should this have anything passed in?
        self.assertEqual(self.hand.cardsInHand.size(), startSize - 1)
        self.hand.updateValidPlay()
        #How to assert that play list has been updated properly?

    def tearDown(self):
        self.assertEqual(self.hand.cardsInHand.size(), 0)
        del self.hand

if __name__ == "__main__":
    unittest.main()