import unittest
from game_objects.CallRules import CallRules
from game_objects.Card import Card
from game_objects.Player import Player

class CallRuleTest(unittest.TestCase):

    def setUp(self):
        self.test_call_rule_tree = CallRules()
        self.temp_player = Player(None, 0, None)
        self.temp_player.rule_tree = self.test_call_rule_tree #how should we let the player know about the rules?

    def test_can_call_first_trick(self):
        self.temp_player.accept(Card(0, "trump")) #give the player the QC
        self.temp_player.accept(Card(2, "trump")) #give the player the QS
        self.temp_player.accept(Card(9, "hearts")) #give the player the AH
        self.temp_player.accept(Card(9, "spades")) #give the player the AS
        self.temp_player.accept(Card(9, "clubs")) #give the player the AC
        self.temp_player._valid_call_list = self.test_call_rule_tree.validate_calls(self.temp_player.get_hand()) #can validate even check one call at a time? do we care?
        self.assertEqual(self.temp_player.get_valid_call_list(), [1,0,0,0,1,1,1,1])

    def test_can_call_ace_of_clubs(self):
        self.temp_player.accept(Card(0, "trump")) #give the player the QC
        self.temp_player.accept(Card(2, "trump")) #give the player the QS
        self.temp_player.accept(Card(9, "hearts")) #give the player the AH
        self.temp_player.accept(Card(9, "spades")) #give the player the AS
        self.temp_player._valid_call_list = self.test_call_rule_tree.validate_calls(self.temp_player.get_hand())
        self.assertEqual(self.temp_player.get_valid_call_list(), [1,1,0,0,0,1,1,1])

    def test_can_call_ace_of_spades(self):
        self.temp_player.accept(Card(0, "trump")) #give the player the QC
        self.temp_player.accept(Card(2, "trump")) #give the player the QS
        self.temp_player.accept(Card(9, "hearts")) #give the player the AH
        self.temp_player.accept(Card(9, "clubs")) #give the player the AS
        self.temp_player._valid_call_list = self.test_call_rule_tree.validate_calls(self.temp_player.get_hand())
        self.assertEqual(self.temp_player.get_valid_call_list(), [1,0,1,0,0,1,1,1])

    def test_can_call_ace_of_hearts(self):
        self.temp_player.accept(Card(0, "trump")) #give the player the QC
        self.temp_player.accept(Card(2, "trump")) #give the player the QS
        self.temp_player.accept(Card(9, "clubs")) #give the player the AH
        self.temp_player.accept(Card(9, "spades")) #give the player the AS
        self.temp_player._valid_call_list = self.test_call_rule_tree.validate_calls(self.temp_player.get_hand())
        self.assertEqual(self.temp_player.get_valid_call_list(), [1,0,0,1,0,1,1,1])

    def test_base_calls(self):
        self.temp_player._valid_call_list = self.test_call_rule_tree.validate_calls(self.temp_player.get_hand())
        self.assertEqual(self.temp_player.get_valid_call_list(), [1,0,0,0,0,1,1,1]) #even if the player has no cards they can make no call or any solo call

    def tearDown(self):
        del self.temp_player
        del self.test_call_rule_tree

if __name__ == "__main__":
    unittest.main()