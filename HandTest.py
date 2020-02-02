import unittest
from GameObjects import *

class HandTest(unittest.TestCase):

    def setUp(self):
        self.testHand = Hand()

    def test_on_init(self):
        self.assertEqual(self.testHand.cardsInHand.size(), 8)
        #How to assert that a valid play list exists and is initialized to true?

    def test_card_played(self):
        startSize = self.testHand.cardsInHand.size()
        self.testHand.playCard() #should this have anything passed in?
        self.assertEqual(self.testHand.cardsInHand.size(), startSize - 1)
        self.testHand.updateValidPlay()
        #How to assert that play list has been updated properly?

    def tearDown(self):
        self.assertEqual(self.testHand.cardsInHand.size(), 0)
        del self.testHand

if __name__ == "__main__":
    unittest.main()