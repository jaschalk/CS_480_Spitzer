from game_objects import Card
import unittest

class CardTest(unittest.TestCase):

    def setUp(self):
        self.testCardTrumpOne = Card.Card(0, "trump")
        self.testCardTrumpTwo = Card.Card(1, "trump")
        self.testCardFailOne = Card.Card(11, "clubs")
        self.testCardFailTwo = Card.Card(12, "clubs")
        self.testCardFailThree = Card.Card(12, "hearts")

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