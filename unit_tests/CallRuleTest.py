import unittest
from game_objects.CallRules import CallRules
from game_objects.Card import Card
from game_objects.Player import Player

class CallRuleTest(unittest.TestCase):

    def setUp(self):
        self.test_call_rule_tree = CallRules()
        self.temp_player = Player(None, 0, None)
        self.temp_player.rule_tree = self.test_call_rule_tree

    def test_can_call_first_trick(self):
        Card(0, "trump").visit(self.temp_player) #give the player the QC
        Card(2, "trump").visit(self.temp_player) #give the player the QS
        Card(9, "hearts").visit(self.temp_player) #give the player the AH
        Card(9, "spades").visit(self.temp_player) #give the player the AS
        Card(9, "clubs").visit(self.temp_player) #give the player the AC
        self.temp_player._valid_call_list = self.test_call_rule_tree.validate_calls(self.temp_player.get_hand())
        self.assertEqual(self.temp_player.get_valid_call_list(), [1,0,0,0,1,1,1,1])

    def test_can_call_ace_of_clubs(self):
        Card(0, "trump").visit(self.temp_player) #give the player the QC
        Card(2, "trump").visit(self.temp_player) #give the player the QS
        Card(9, "hearts").visit(self.temp_player) #give the player the AH
        Card(9, "spades").visit(self.temp_player) #give the player the AS
        self.temp_player._valid_call_list = self.test_call_rule_tree.validate_calls(self.temp_player.get_hand())
        self.assertEqual(self.temp_player.get_valid_call_list(), [1,1,0,0,0,1,1,1])

    def test_can_call_ace_of_spades(self):
        Card(0, "trump").visit(self.temp_player) #give the player the QC
        Card(2, "trump").visit(self.temp_player) #give the player the QS
        Card(9, "hearts").visit(self.temp_player) #give the player the AH
        Card(9, "clubs").visit(self.temp_player) #give the player the AS
        self.temp_player._valid_call_list = self.test_call_rule_tree.validate_calls(self.temp_player.get_hand())
        self.assertEqual(self.temp_player.get_valid_call_list(), [1,0,1,0,0,1,1,1])

    def test_can_call_ace_of_hearts(self):
        Card(0, "trump").visit(self.temp_player) #give the player the QC
        Card(2, "trump").visit(self.temp_player) #give the player the QS
        Card(9, "clubs").visit(self.temp_player) #give the player the AH
        Card(9, "spades").visit(self.temp_player) #give the player the AS
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