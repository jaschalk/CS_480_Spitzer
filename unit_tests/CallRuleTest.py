import unittest
from game_objects import CallRules as CR
from game_objects import Card
from game_objects import Hand
from game_objects import Player

class CallRuleTest(unittest.TestCase):

    def setUp(self):
        self.test_call_rule_tree = CR.CallRules()
        self.temp_player = Player.Player(0)
        self.temp_player.rule_tree = self.test_call_rule_tree #how should we let the player know about the rules?

    def test_can_call_first_trick(self):
        self.temp_player.accept(Card.Card(0, "trump")) #give the player the QC
        self.temp_player.accept(Card.Card(2, "trump")) #give the player the QS
        self.temp_player.accept(Card.Card(9, "hearts")) #give the player the AH
        self.temp_player.accept(Card.Card(9, "spades")) #give the player the AS
        self.temp_player.accept(Card.Card(9, "clubs")) #give the player the AC
        self.test_call_rule_tree.validate(self.temp_player) #can validate even check one call at a time? do we care?
        self.assertEqual(self.temp_player.get_valid_call_list(), [1,0,0,0,1,1,1,1])

    def test_can_call_ace_of_clubs(self):
        self.temp_player.accept(Card.Card(0, "trump")) #give the player the QC
        self.temp_player.accept(Card.Card(2, "trump")) #give the player the QS
        self.temp_player.accept(Card.Card(9, "hearts")) #give the player the AH
        self.temp_player.accept(Card.Card(9, "spades")) #give the player the AS
        self.test_call_rule_tree.validate(self.temp_player)
        self.assertEqual(self.temp_player.get_valid_call_list(), [1,1,0,0,0,1,1,1])

    def test_can_call_ace_of_spades(self):
        self.temp_player.accept(Card.Card(0, "trump")) #give the player the QC
        self.temp_player.accept(Card.Card(2, "trump")) #give the player the QS
        self.temp_player.accept(Card.Card(9, "hearts")) #give the player the AH
        self.temp_player.accept(Card.Card(9, "clubs")) #give the player the AS
        self.test_call_rule_tree.validate(self.temp_player)
        self.assertEqual(self.temp_player.get_valid_call_list(), [1,0,1,0,0,1,1,1])

    def test_can_call_ace_of_hearts(self):
        self.temp_player.accept(Card.Card(0, "trump")) #give the player the QC
        self.temp_player.accept(Card.Card(2, "trump")) #give the player the QS
        self.temp_player.accept(Card.Card(9, "clubs")) #give the player the AH
        self.temp_player.accept(Card.Card(9, "spades")) #give the player the AS
        self.test_call_rule_tree.validate(self.temp_player)
        self.assertEqual(self.temp_player.get_valid_call_list(), [1,0,0,1,0,1,1,1])

    def test_base_calls(self):
        self.test_call_rule_tree.validate(self.temp_player)
        self.assertEqual(self.temp_player.get_valid_call_list(), [1,0,0,0,0,1,1,1]) #even if the player has no cards they can make no call or any solo call

    def tearDown(self):
        del self.temp_player
        del self.test_call_rule_tree

if __name__ == "__main__":
    unittest.main()