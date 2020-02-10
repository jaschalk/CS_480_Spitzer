import unittest
from GameObjects import *

class CardRuleTest(unittest.TestCase):

    def setUp(self):
        self.test_tree = CardRuleTree

    def tearDown(self):
        del self.test_tree

if __name__ == "__main__":
    unittest.main()