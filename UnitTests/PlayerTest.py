import unittest
from GameObjects import *

class PlayerTest(unittest.TestCase):

    def setUp(self):
       self.testPlayer = Player()

    def test_on_init(self):
        self.assertEqual(self.testPlayer.roundScore, 0)
        self.assertEqual(self.testPlayer.totalScore, 0)
        self.assertFalse(self.testPlayer.isLeading)
        self.assertEqual(self.testPlayer.potentialPartnersList, 4)
        #How to test if it is initialized with the values 1/3, 1/3, 1/3, and 1?

    def test_after_delt(self):
        #Need to test if the player already has a hand. If not, needs to create one after being delt cards? How?

    def test_trick_complete(self):
        #Need to test that on completion of a trick, the potential partners list is updated.
     

    if __name__ == "__main__":
        unittest.main()