import unittest
from unit_tests.Setup import general_setup
from game_objects.CardRuleTree import CardRuleTree as CRT
from game_objects.Player import Player
from game_objects.Round import Round
from game_objects.Trick import Trick
from game_objects.Card import Card

class CardRuleTest(unittest.TestCase):

    def setUp(self):
        setup_results = general_setup()
        self.test_tree = setup_results["card_rules"]
        self.temp_round = setup_results["current_round"]
        self.temp_trick = setup_results["current_trick"]
        self.temp_player = setup_results["list_of_players"][0]
        self.temp_round.set_leading_player(setup_results["list_of_players"][1])
        self.card_list = []
        for i in range(15):
            self.card_list.append(Card(i, "trump"))
        for i in range(9,15):
            self.card_list.append(Card(i, "clubs"))
        for i in range(9,15):
            self.card_list.append(Card(i, "spades"))
        for i in range(9,15):
            self.card_list.append(Card(i, "hearts"))
        del setup_results

    def test_is_leading(self):
        self.temp_round.set_leading_player(self.temp_player)
        for card in self.card_list:
            self.assertTrue(self.temp_player.validate_card(card))

    def test_can_follow_suit(self):
        self.temp_trick.accept(self.card_list[15]) # put the Ace of Clubs on the trick
        for i in range(16,25): # give the player 8 cards: 10C, KC, 9C, 8C, 7C, AS, 10S, KS
            self.temp_player.accept(self.card_list[i])
        self.assertTrue(self.temp_player.validate_card(self.temp_player.get_hand().get_cards_in_hand()[0]))
        self.assertTrue(self.temp_player.validate_card(self.temp_player.get_hand().get_cards_in_hand()[1]))
        self.assertTrue(self.temp_player.validate_card(self.temp_player.get_hand().get_cards_in_hand()[2]))
        self.assertTrue(self.temp_player.validate_card(self.temp_player.get_hand().get_cards_in_hand()[3]))
        self.assertTrue(self.temp_player.validate_card(self.temp_player.get_hand().get_cards_in_hand()[4]))
        self.assertFalse(self.temp_player.validate_card(self.temp_player.get_hand().get_cards_in_hand()[5]))
        self.assertFalse(self.temp_player.validate_card(self.temp_player.get_hand().get_cards_in_hand()[6]))
        self.assertFalse(self.temp_player.validate_card(self.temp_player.get_hand().get_cards_in_hand()[7]))
        for i in range(len(self.temp_player.get_hand().get_cards_in_hand())):
            if i < 5: # the first 5 cards in the players hand are clubs and should be valid to play
                self.assertTrue(self.temp_player.validate_card(self.temp_player.get_hand().get_cards_in_hand()[i]))
            else: # all remaining cards in the players hand are spades and should not be valid to play
                self.assertFalse(self.temp_player.validate_card(self.temp_player.get_hand().get_cards_in_hand()[i]))

    def test_cannot_follow_suit_has_trump(self):
        self.temp_trick.accept(self.card_list[31]) # put the 7H on the trick
        for i in range(11,19): # give 8 cards to the player: KD, 9D, 8D, AC, 10C, KC, 9C, 8C
            self.temp_player.accept(self.card_list[i])
        for i in range(len(self.temp_player.get_hand().get_cards_in_hand())):
            if i < 3: # the first 3 cards in the players hand are trump and should be playable
                self.assertTrue(self.temp_player.validate_card(self.temp_player.get_hand().get_cards_in_hand()[i]))
            else: # all remaining cards in the players hand are not trump or the suit lead and should not be playable
                self.assertFalse(self.temp_player.validate_card(self.temp_player.get_hand().get_cards_in_hand()[i]))

    def test_cannot_follow_suit_has_no_trump(self):
        self.temp_trick.accept(self.card_list[31]) # put the 7H on the trick
        for i in range(16,24): # give the player 8 cards: 10C, KC, 9C, 8C, 7C, AS, 10S, KS
            self.temp_player.accept(self.card_list[i])
        self.assertTrue(self.temp_player.validate_card(self.temp_player.get_hand().get_cards_in_hand()[0]))
        self.assertTrue(self.temp_player.validate_card(self.temp_player.get_hand().get_cards_in_hand()[1]))
        self.assertTrue(self.temp_player.validate_card(self.temp_player.get_hand().get_cards_in_hand()[2]))
        self.assertTrue(self.temp_player.validate_card(self.temp_player.get_hand().get_cards_in_hand()[3]))
        self.assertTrue(self.temp_player.validate_card(self.temp_player.get_hand().get_cards_in_hand()[4]))
        self.assertTrue(self.temp_player.validate_card(self.temp_player.get_hand().get_cards_in_hand()[5]))
        self.assertTrue(self.temp_player.validate_card(self.temp_player.get_hand().get_cards_in_hand()[6]))
        self.assertTrue(self.temp_player.validate_card(self.temp_player.get_hand().get_cards_in_hand()[7]))
        for i in range(len(self.temp_player.get_hand().get_cards_in_hand())):
            self.assertTrue(self.temp_player.validate_card(self.temp_player.get_hand().get_cards_in_hand()[i]))

    def test_ace_called_and_player_has_called_ace_with_suit_lead(self):
        self.temp_round._call_matrix[1][3] = 1 # force the round to have the second player have called the ace of hearts
        self.temp_trick.accept(self.card_list[31]) # put the 7H on the trick
        for i in range(22,30): # give the player 8 cards: KS,9S,8S,7S,AH,10H,KH,9H
            self.temp_player.accept(self.card_list[i])
        self.assertFalse(self.temp_player.validate_card(self.temp_player.get_hand().get_cards_in_hand()[0]))
        self.assertFalse(self.temp_player.validate_card(self.temp_player.get_hand().get_cards_in_hand()[1]))
        self.assertFalse(self.temp_player.validate_card(self.temp_player.get_hand().get_cards_in_hand()[2]))
        self.assertFalse(self.temp_player.validate_card(self.temp_player.get_hand().get_cards_in_hand()[3]))
        self.assertFalse(self.temp_player.validate_card(self.temp_player.get_hand().get_cards_in_hand()[4]))
        self.assertTrue(self.temp_player.validate_card(self.temp_player.get_hand().get_cards_in_hand()[5]))
        self.assertFalse(self.temp_player.validate_card(self.temp_player.get_hand().get_cards_in_hand()[6])) 
        self.assertFalse(self.temp_player.validate_card(self.temp_player.get_hand().get_cards_in_hand()[7]))
        for i in range(len(self.temp_player.get_hand().get_cards_in_hand())):
            if i != 5:
                self.assertFalse(self.temp_player.validate_card(self.temp_player.get_hand().get_cards_in_hand()[i]))
            else: # since the player has the ace and that suit was lead only that ace is a valid card to play
                self.assertTrue(self.temp_player.validate_card(self.temp_player.get_hand().get_cards_in_hand()[i]))

    def test_ace_called_and_player_has_called_ace_with_suit_not_lead(self): 
        self.temp_round.get_call_matrix()[1][3] = 1 # force the round to have the second player have called the ace of hearts
        self.temp_trick.accept(self.card_list[14]) # put the AC on the trick
        for i in range(22,30): # give the player 8 cards: KS,9S,8S,7S,AH,10H,KH,9H
            self.temp_player.accept(self.card_list[i])
        for i in range(len(self.temp_player.get_hand().get_cards_in_hand())):
            if i == 5: # since the player has the ace called and that suit was not lead that ace is not a valid card to play
                self.assertFalse(self.temp_player.validate_card(self.temp_player.get_hand().get_cards_in_hand()[i]))
            else: # all other cards are valid here since this player doesn't have trump or the suit lead
                self.assertTrue(self.temp_player.validate_card(self.temp_player.get_hand().get_cards_in_hand()[i]))

    def tearDown(self):
        for card in self.card_list:
            del card
        del self.card_list
        del self.temp_player
        del self.test_tree

#             index 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 ,10, 11,12,13,14,15,16,17,18,19, 20,21,22,23,24,25, 26,27,28,29,30,31
#32 cards in order: QC,7D,QS,QH,QD,JC,JS,JH,JD,AD,10D,KD,9D,8D,(A,10,K ,9 ,8 ,7)C,(A,10,K ,9 ,8 ,7)S,(A,10,K ,9 ,8 ,7)H
#              rank 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11,12,13, 9,10,11,12,13,14,  9,10,11,12,13,14,  9,10,11,12,13,14
#      index - rank 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,   0, 0, 0, 5, 5, 5, 5, 5, 5, 11,11,11,11,11,11, 17,17,17,17,17,17
#   index = rank + suit_offset: C=5, S=11, H=17
if __name__ == "__main__":
    unittest.main()