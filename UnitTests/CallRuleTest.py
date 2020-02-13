import unittest
from GameObjects import CallRules as CR
from GameObjects import Card
from GameObjects import Hand
from GameObjects import Player

class CallRuleTest(unittest.TestCase):

    def setUp(self):
        self.test_call_rule_tree = CR.CallRules()
        self.temp_player = Player.Player(0)
        self.temp_player.rule_tree = self.test_call_rule_tree
        

    def test_can_call_first_trick(self):
        self.temp_player.accept(Card.Card(0, "trump")) #give the player the QC
        self.temp_player.accept(Card.Card(2, "trump")) #give the player the QS
        self.temp_player.accept(Card.Card(9, "hearts")) #give the player the AH
        self.temp_player.accept(Card.Card(9, "spades")) #give the player the AS
        self.temp_player.accept(Card.Card(9, "clubs")) #give the player the AC
        self.temp_player.evaluate_calls() #since we're now expecting the player the hold on to the rule trees some method like this should work
        self.assertEqual(self.temp_player.valid_call_list, [1,1,0,0,0,1,1,1])

    def test_can_call_ace_of_clubs(self):
        self.temp_player.accept(Card.Card(0, "trump")) #give the player the QC
        self.temp_player.accept(Card.Card(2, "trump")) #give the player the QS
        self.temp_player.accept(Card.Card(9, "hearts")) #give the player the AH
        self.temp_player.accept(Card.Card(9, "spades")) #give the player the AS
        self.temp_player.evaluate_calls() #since we're now expecting the player the hold on to the rule trees some method like this should work
        self.assertEqual(self.temp_player.valid_call_list, [1,0,1,0,0,1,1,1])

    def test_can_call_ace_of_spades(self):
        self.temp_player.accept(Card.Card(0, "trump")) #give the player the QC
        self.temp_player.accept(Card.Card(2, "trump")) #give the player the QS
        self.temp_player.accept(Card.Card(9, "hearts")) #give the player the AH
        self.temp_player.accept(Card.Card(9, "clubs")) #give the player the AS
        self.temp_player.evaluate_calls() #since we're now expecting the player the hold on to the rule trees some method like this should work
        self.assertEqual(self.temp_player.valid_call_list, [1,0,0,1,0,1,1,1])

    def test_can_call_ace_of_hearts(self):
        self.temp_player.accept(Card.Card(0, "trump")) #give the player the QC
        self.temp_player.accept(Card.Card(2, "trump")) #give the player the QS
        self.temp_player.accept(Card.Card(9, "clubs")) #give the player the AH
        self.temp_player.accept(Card.Card(9, "spades")) #give the player the AS
        self.temp_player.evaluate_calls() #since we're now expecting the player the hold on to the rule trees some method like this should work
        self.assertEqual(self.temp_player.valid_call_list, [1,0,0,0,1,1,1,1])

    def test_base_calls(self):
        self.temp_player.evaluate_calls() #since we're now expecting the player the hold on to the rule trees some method like this should work
        self.assertEqual(self.temp_player.valid_call_list, [1,0,0,0,0,1,1,1]) #even if the player has no cards they can make no call or any solo call

    def tearDown(self):
        del self.temp_player
        del self.test_call_rule_tree

if __name__ == "__main__":
    unittest.main()