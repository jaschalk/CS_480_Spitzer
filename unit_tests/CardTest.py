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
        self.assertFalse(self.testCardFailOne.accept(self.testCardTrumpOne))

    def test_trump_receives_fail(self):
        self.assertTrue(self.testCardTrumpOne.accept(self.testCardFailOne))

    def test_trump_receives_trump(self):
        self.assertTrue(self.testCardTrumpOne.accept(self.testCardTrumpTwo))
    
    def test_fail_receives_fail_same(self):
        self.assertTrue(self.testCardFailOne.accept(self.testCardFailTwo))

    def test_fail_receives_fail_different(self):
        self.assertTrue(self.testCardFailOne.accept(self.testCardFailThree))

if __name__ == "__main__":
    unittest.main()