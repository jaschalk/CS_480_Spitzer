import unittest
from unit_tests.Setup import general_setup
from game_objects.Hand import Hand
from game_objects.Card import Card

class PlayerTest(unittest.TestCase):

    def setUp(self):
        setup_results = general_setup()
        self.temp_player_list = setup_results["list_of_players"]
        self.temp_player_zero = self.temp_player_list[0]
        self.temp_round = setup_results["current_round"]
        self.test_hand = setup_results["player_zero_hand"]
        self.current_trick = setup_results["current_trick"]

    def test_on_init(self):
        self.assertEqual(self.temp_player_zero.get_round_score(), 0)
        self.assertEqual(self.temp_player_zero.get_total_score(), 0)
        self.assertFalse(self.temp_player_zero.get_is_leading())
        self.assertIsInstance(self.temp_player_zero.get_hand(), Hand)
        self.assertEqual(len(self.temp_player_zero.get_valid_call_list()), 8)
        self.assertEqual(len(self.temp_player_zero.get_potential_partners_list()), 4)
        self.assertEqual(self.temp_player_zero.get_potential_partners_list()[0], 1)
        for index in range(1,4):
            self.assertAlmostEqual(self.temp_player_zero.get_potential_partners_list()[index], 1/3)

    def test_trick_complete(self):
        current_round_score = self.temp_player_zero.get_round_score()
        for index in range(4):
            self.temp_player_list[index].accept(Card(index, "trump"))
            self.temp_player_list[index].play_card_to(self.current_trick)
        self.assertEqual(self.temp_player_zero.get_round_score(), 9)
        self.assertEqual(self.temp_player_zero.get_round_score(), (current_round_score + self.temp_player_zero.get_trick_score()))
        self.assertEqual(self.temp_player_list[0].get_potential_partners_list(), [1,0,1,0])
        self.assertEqual(self.temp_player_list[1].get_potential_partners_list(), [0,1,0,1])
        self.assertEqual(self.temp_player_list[2].get_potential_partners_list(), [1,0,1,0])
        self.assertEqual(self.temp_player_list[3].get_potential_partners_list(), [0,1,0,1])

    def test_card_acceptance(self):
        for index in range(5):
            self.temp_player_zero.accept(Card(index, "trump"))
        #This trump card is not what we are expecting it to be.
        self.assertEqual(self.temp_player_zero.get_hand().get_cards_in_hand()[4], Card(4, "trump")) 
    
    #Create a test to test a method calling upon the tree to modify the Players' potential partners lists.
    def test_no_call_is_made(self):
        #self.temp_player_zero.ask_for_call(0)
        self.assertEqual(self.temp_player_zero.get_potential_partners_list()[0], 1)
        for index in range(1,4):
            self.assertAlmostEqual(self.temp_player_zero.get_potential_list()[index], 1/3)

    def tearDown(self):
        #for index in range(4): #for some reason, this is saying that the list index is out of range.
            #del self.temp_player_list[index]
        del self.temp_player_list

if __name__ == "__main__":
    unittest.main()