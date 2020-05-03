import unittest
from game_objects.Card import Card
from unit_tests.Setup import general_setup

class PartnerRuleTest(unittest.TestCase):

    def setUp(self):
        setup_results = general_setup()
        self.temp_game = setup_results["active_game"]
        self.temp_deck = setup_results["game_deck"]
        self.temp_player_list = setup_results["list_of_players"]
        self.temp_round = setup_results["current_round"]
        self.test_hand = setup_results["player_zero_hand"]
        self.current_trick = setup_results["current_trick"]
        self.card_list = []
        for index in range(14):
            self.card_list.append(Card(index, "trump"))
        for index in range(9,15):
            self.card_list.append(Card(index, "clubs"))
        for index in range(9,15):
            self.card_list.append(Card(index, "spades"))
        for index in range(9,15):
            self.card_list.append(Card(index, "hearts"))
        del setup_results

    def test_first_trick_called(self):
        for index in range(5):
            self.card_list[index].visit(self.temp_player_list[0]) #give the first player the first 5 trump cards ,includes both queens
        self.card_list[14].visit(self.temp_player_list[0]) #give the first player all 3 fail aces
        self.card_list[20].visit(self.temp_player_list[0])
        self.card_list[26].visit(self.temp_player_list[0])
        for index in range(5, 13):
            self.card_list[index].visit(self.temp_player_list[1]) #give the second player the next 8 trump cards
        for index in range(13, 23):
            if index != 14:
                if index != 20:
                    self.card_list[index].visit(self.temp_player_list[2]) #give the third player the next 8 cards, skipping any aces
                else:
                    continue
        for index in range(23, 32):
            if index != 26:
                self.card_list[index].visit(self.temp_player_list[3]) #give the fourth player the last 8 cards, skipping any aces
            else:
                continue
        self.temp_round.update_call(self.temp_player_list[0].get_player_id(), 4)
        self.temp_player_list[0].get_hand().play_card_at_index(self.current_trick, 6) #AS
        self.temp_player_list[1].get_hand().play_card_at_index(self.current_trick, 7) #9D -- player 2 wins the trick
        self.temp_player_list[2].get_hand().play_card_at_index(self.current_trick, 7) #KS
        self.temp_player_list[3].get_hand().play_card_at_index(self.current_trick, 0) #9S
        for index in range(4):
            self.temp_player_list[index].determine_potential_partners()
        self.assertEqual(self.temp_player_list[0].get_potential_partners_list(), [1,1,0,0])
        self.assertEqual(self.temp_player_list[1].get_potential_partners_list(), [1,1,0,0])
        self.assertEqual(self.temp_player_list[2].get_potential_partners_list(), [0,0,1,1])
        self.assertEqual(self.temp_player_list[3].get_potential_partners_list(), [0,0,1,1])

    def test_ace_called(self):
        self.card_list[0].visit(self.temp_player_list[0]) #give player 1 both black queens and 7, 8, 9 of spades and hearts
        self.card_list[2].visit(self.temp_player_list[0])
        for index in range(12, 15):
            Card(index, "spades").visit(self.temp_player_list[0])
            Card(index, "hearts").visit(self.temp_player_list[0])
        for index in range(9, 11):
            Card(index, "trump").visit(self.temp_player_list[1]) #give player 2 all aces and 10s
            Card(index, "clubs").visit(self.temp_player_list[1])
            Card(index, "spades").visit(self.temp_player_list[1])
            Card(index, "hearts").visit(self.temp_player_list[1])
        for index in range(3, 9):
            Card(index, "trump").visit(self.temp_player_list[2]) #give player 3 a bunch of random trump cards
        self.card_list[1].visit(self.temp_player_list[2]) #spitzer
        self.card_list[11].visit(self.temp_player_list[2]) #KD
        self.temp_round.update_call(self.temp_player_list[0].get_player_id(), 1)
        for index in range(4):
            self.temp_player_list[index].determine_potential_partners()
        self.assertEqual(self.temp_player_list[1].get_potential_partners_list(), [1,1,0,0])
        self.assertEqual(self.temp_player_list[0].get_potential_partners_list()[0], 1)
        for index in range(1,4):
            self.assertAlmostEqual(self.temp_player_list[0].get_potential_partners_list()[index], 1/3)

    def test_solo_called(self):
        self.temp_round.update_call(self.temp_player_list[0].get_player_id(), 5)
        for index in range(4):
            self.temp_player_list[index].determine_potential_partners()
        self.assertEqual(self.temp_player_list[0].get_potential_partners_list(), [1,0,0,0])
        self.assertEqual(self.temp_player_list[1].get_potential_partners_list(), [0,1,1,1])
        self.assertEqual(self.temp_player_list[2].get_potential_partners_list(), [0,1,1,1])
        self.assertEqual(self.temp_player_list[3].get_potential_partners_list(), [0,1,1,1])

    def test_no_call_both_queens(self):
        for index in range(8):
            self.card_list[index].visit(self.temp_player_list[0]) #Give player 1 the first 8 cards
        self.temp_round.update_call(self.temp_player_list[0].get_player_id(), 0)
        self.temp_player_list[0].determine_potential_partners()
        self.assertEqual(self.temp_player_list[0].get_potential_partners_list(), [1,0,0,0])

    def test_no_call_one_queen_played(self):
        self.card_list[0].visit(self.temp_player_list[0]) #QC
        self.card_list[2].visit(self.temp_player_list[1]) #QS
        self.card_list[1].visit(self.temp_player_list[1]) #7D
        self.card_list[30].visit(self.temp_player_list[2]) #8H
        self.card_list[31].visit(self.temp_player_list[3]) #7H
        self.temp_player_list[0].get_hand().play_card_at_index(self.current_trick, 0) #QC
        self.temp_player_list[1].get_hand().play_card_at_index(self.current_trick, 1) #7D
        self.temp_player_list[2].get_hand().play_card_at_index(self.current_trick, 0) #8H
        self.temp_player_list[3].get_hand().play_card_at_index(self.current_trick, 0) #7H
        self.temp_round.update_call(self.temp_player_list[0].get_player_id(), 0)
        for index in range(4):
            self.temp_player_list[index].determine_potential_partners()
        self.assertEqual(self.temp_player_list[0].get_potential_partners_list()[0], 1)
        for index in range(1,4):
            self.assertAlmostEqual(self.temp_player_list[0].get_potential_partners_list()[index], 1/3)
        self.assertEqual(self.temp_player_list[1].get_potential_partners_list(), [1,1,0,0])
        self.assertEqual(self.temp_player_list[2].get_potential_partners_list()[0], 0)
        self.assertAlmostEqual(self.temp_player_list[2].get_potential_partners_list()[1], 1/2)
        self.assertEqual(self.temp_player_list[2].get_potential_partners_list()[2], 1)
        self.assertAlmostEqual(self.temp_player_list[2].get_potential_partners_list()[3], 1/2)
        self.assertEqual(self.temp_player_list[3].get_potential_partners_list()[0], 0)
        self.assertAlmostEqual(self.temp_player_list[3].get_potential_partners_list()[1], 1/2)
        self.assertAlmostEqual(self.temp_player_list[3].get_potential_partners_list()[2], 1/2)
        self.assertEqual(self.temp_player_list[3].get_potential_partners_list()[3], 1)

    def test_no_call_no_queen_played(self):
        self.card_list[0].visit(self.temp_player_list[0])
        self.card_list[3].visit(self.temp_player_list[0])
        self.card_list[2].visit(self.temp_player_list[1])
        self.card_list[1].visit(self.temp_player_list[1])
        self.card_list[30].visit(self.temp_player_list[2])
        self.card_list[29].visit(self.temp_player_list[2])
        self.card_list[31].visit(self.temp_player_list[3])
        self.card_list[28].visit(self.temp_player_list[3])
        self.temp_player_list[0].get_hand().play_card_at_index(self.current_trick, 1) #QH
        self.temp_player_list[1].get_hand().play_card_at_index(self.current_trick, 1) #7D
        self.temp_player_list[2].get_hand().play_card_at_index(self.current_trick, 0) #8H
        self.temp_player_list[3].get_hand().play_card_at_index(self.current_trick, 0) #7H
        self.temp_round.update_call(self.temp_player_list[0].get_player_id(), 0)
        for index in range(4):
            self.temp_player_list[index].determine_potential_partners()
        for index in range(4):
            self.assertEqual(self.temp_player_list[index].get_potential_partners_list()[index], 1)
            for i in range(4):
                if (i != index):
                    self.assertAlmostEqual(self.temp_player_list[index].get_potential_partners_list()[i], 1/3)

    def tearDown(self):
        del self.temp_game
        del self.temp_deck
        del self.temp_player_list
        del self.temp_round
        del self.test_hand
        del self.current_trick
        del self.card_list

if __name__ == "__main__":
    unittest.main()