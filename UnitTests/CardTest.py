import unittest
from GameObjects import *

class CardTest(unittest.TestCase):

    def setUp(self):
        self.testCardTrumpOne = Card(0, "trump")
        self.testCardTrumpTwo = Card(1, "trump")
        self.testCardFailOne = Card(11, "clubs")
        self.testCardFailTwo = Card(12, "clubs")
        self.testCardFailThree = Card(12, "hearts")

    def test_fail_receives_trump(self):
        self.testCardFailOne.accept(self.testCardTrumpOne)
        self.assertFalse(self.testCardFailOne.wins()) #have wins return a boolean of whether or not the card wins.

    def test_trump_receives_fail(self):
        self.testCardTrumpOne.accept(self.testCardFailOne)
        self.assertTrue(self.testCardTrumpOne.wins())

    def test_trump_receives_trump(self):
        self.testCardTrumpOne.accept(self.testCardTrumpTwo)
        self.assertTrue(self.testCardTrumpOne.wins())
    
    def test_fail_receives_fail_same(self):
        self.testCardFailOne.accept(self.testCardFailTwo)
        self.assertTrue(self.testCardFailOne.wins())

    def test_fail_receives_fail_different(self):
        self.testCardFailOne.accept(self.testCardFailThree)
        self.assertTrue(self.testCardFailOne.wins())

if __name__ == "__main__":
    unittest.main()