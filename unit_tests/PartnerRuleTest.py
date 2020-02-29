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
    
    def test_first_trick_called(self):
        for index in range(5):
            self.temp_player_list[0].accept(self.card_list[index]) #give the first player the first 5 trump cards (includes both queens)
        self.temp_player_list[0].accept(self.card_list[14]) #give the first player all 3 fail aces
        self.temp_player_list[0].accept(self.card_list[20])
        self.temp_player_list[0].accept(self.card_list[26])
        for index in range(5, 13):
            self.temp_player_list[1].accept(self.card_list[index]) #give the second player the next 8 trump cards
        for index in range(13, 23):
            if index != 14:
                if index != 20:
                    self.temp_player_list[2].accept(self.card_list[index]) #give the third player the next 8 cards, skipping any aces
                else:
                    continue
        for index in range(23, 32):
            if index != 26:
                self.temp_player_list[3].accept(self.card_list[index]) #give the fourth player the last 8 cards, skipping any aces
            else:
                continue
        self.temp_player_list[0].makeCall(4)
        self.temp_player_list[0].hand.playCard(20, self.current_trick) #AS
        self.temp_player_list[1].hand.playCard(13, self.current_trick) #8D player 2 wins the trick
        self.temp_player_list[2].hand.playCard(22, self.current_trick) #KS
        self.temp_player_list[3].hand.playCard(23, self.current_trick) #9S
        self.assertEqual(self.temp_player_list[0].potentialPartnersList, [1,1,0,0])
        self.assertEqual(self.temp_player_list[1].potentialPartnersList, [1,1,0,0])
        self.assertEqual(self.temp_player_list[1].potentialPartnersList, [0,0,1,1])
        
    def test_ace_called(self):
        self.temp_player_list[0].accept(self.card_list[0]) #give player 1 both black queens and 7, 8, 9 of spades and hearts
        self.temp_player_list[0].accept(self.card_list[2])
        for index in range(12, 15):
            self.temp_player_list[0].accept(Card(index, "spades"))
            self.temp_player_list[0].accept(Card(index, "hearts"))
        for index in range(9, 11):
            self.temp_player_list[1].accept(Card(index, "trump")) #give player 2 all aces and 10s
            self.temp_player_list[1].accept(Card(index, "clubs"))
            self.temp_player_list[1].accept(Card(index, "spades"))
            self.temp_player_list[1].accept(Card(index, "hearts"))
        for index in range(3, 9):
            self.temp_player_list[2].accept(Card(index, "trump")) #give player 3 a bunch of random trump cards
        self.temp_player_list[2].accept(self.card_list[1]) #spitzer
        self.temp_player_list[2].accept(self.card_list[11]) #KD
        self.temp_player_list[0].makeCall(3)
        self.assertEqual(self.temp_player_list[1].potentialPartnersList, [1,1,0,0]) #Only update the potential partners list of the player with the ace matching the one called.
        self.assertEqual(self.temp_player_list[0].potentialPartnersList[0], 1)
        for index in range(1,4):
            self.assertAlmostEqual(self.temp_player_list[0].potentialPartnersList[index], 1/3)

    def test_solo_called(self):
        self.temp_player_list[0].makeCall(5)
        self.assertEqual(self.temp_player_list[0].potentialPartnersList, [1,0,0,0])
        self.assertEqual(self.temp_player_list[1].potentialPartnersList, [0,1,1,1])
        self.assertEqual(self.temp_player_list[2].potentialPartnersList, [0,1,1,1])
        self.assertEqual(self.temp_player_list[3].potentialPartnersList, [0,1,1,1])

    def test_no_call_both_queens(self):
        for index in range(8):
            self.temp_player_list[0].accept(self.card_list[index]) #Give player 1 the first 8 cards
        self.assertEqual(self.temp_player_list[0].potentialPartnersList, [1,0,0,0])

    def test_no_call_one_queen_played(self):
        self.temp_player_list[0].accept(self.card_list[0])
        self.temp_player_list[1].accept(self.card_list[2])
        self.temp_player_list[1].accept(self.card_list[1])
        self.temp_player_list[2].accept(self.card_list[30])
        self.temp_player_list[3].accept(self.card_list[31])
        self.temp_player_list[0].hand.playCard(0, self.current_trick) 
        self.temp_player_list[1].hand.playCard(1, self.current_trick)
        self.temp_player_list[2].hand.playCard(30, self.current_trick)
        self.temp_player_list[3].hand.playCard(31, self.current_trick)
        self.assertEqual(self.temp_player_list[0].potentialPartnersList[0], 1)
        for index in range(1,4):
            self.assertAlmostEqual(self.temp_player_list[0].potentialPartnersList[index], 1/3)
        self.assertEqual(self.temp_player_list[1].potentialPartnersList, [1,1,0,0])
        self.assertEqual(self.temp_player_list[2].potentialPartnersList[0], 0)
        self.assertAlmostEqual(self.temp_player_list[2].potentialPartnersList[1], 1/2)
        self.assertEqual(self.temp_player_list[2].potentialPartnersList[2], 1)
        self.assertAlmostEqual(self.temp_player_list[2].potentialPartnersList[3], 1/2)
        self.assertEqual(self.temp_player_list[3].potentialPartnersList[0], 0)
        self.assertAlmostEqual(self.temp_player_list[3].potentialPartnersList[1], 1/2)
        self.assertAlmostEqual(self.temp_player_list[3].potentialPartnersList[2], 1/2)
        self.assertEqual(self.temp_player_list[3].potentialPartnersList[3], 1)
        
    def test_no_call_no_queen_played(self):
        self.temp_player_list[0].accept(self.card_list[0])
        self.temp_player_list[0].accept(self.card_list[3])
        self.temp_player_list[1].accept(self.card_list[2])
        self.temp_player_list[1].accept(self.card_list[1])
        self.temp_player_list[2].accept(self.card_list[30])
        self.temp_player_list[2].accept(self.card_list[29])
        self.temp_player_list[3].accept(self.card_list[31])
        self.temp_player_list[3].accept(self.card_list[28])
        self.temp_player_list[0].hand.playCard(3, self.current_trick) 
        self.temp_player_list[1].hand.playCard(1, self.current_trick)
        self.temp_player_list[2].hand.playCard(30, self.current_trick)
        self.temp_player_list[3].hand.playCard(31, self.current_trick)
        for index in range(4):
            self.assertEqual(self.temp_player_list[index].potentialPartnersList[index], 1)
            for i in range(4):
                self.assertAlmostEqual(self.temp_player_list[index].potentialPartnersList[i], 1/3)

if __name__ == "__main__":
    unittest.main()