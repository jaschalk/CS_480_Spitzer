import unittest
from GameObjects import *

class CardTest(unittest.TestCase):

    def setUp(self):
        self.testCard = Card()

    #How to test visitation method? Don't remember if we talked about this.

    #Are we testing the visitor or the acceptor? Current tests are set up for acceptor.
    def test_fail_receives_trump(self):
        self.assertFalse(self.testCard.wins())

    def test_trump_receives_fail(self):
        self.assertTrue(self.testCard.wins())

    def test_trump_receives_trump(self):
        winner = self.testCard.compareRank() #have this method return the card with the higher rank?
        self.assertTrue(winner.wins())
    
    def test_fail_receives_fail_same(self):
        winner = self.testCard.compareRank()
        self.assertTrue(winner.wins())

    def test_fail_receives_fail_different(self):
        self.assertTrue(self.testCard.wins())

if __name__ == "__main__":
    unittest.main()