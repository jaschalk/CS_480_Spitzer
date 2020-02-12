import unittest
from GameObjects import CardRuleTree as CRT
from GameObjects import Player
from GameObjects import Round
from GameObjects import Trick
from GameObjects import Card

class CardRuleTest(unittest.TestCase):

    def setUp(self):
        self.test_tree = CRT.CardRuleTree()
        self.temp_round = Round.Round(0)
        self.temp_trick = Trick.Trick(self.temp_round, None)
        self.temp_round.current_trick = self.temp_trick
        self.temp_player = Player.Player(0)
        self.card_list = []
        for i in range(15):
            self.card_list.append(Card.Card(i, "trump"))
        for i in range(9,15):
            self.card_list.append(Card.Card(i, "clubs"))
        for i in range(9,15):
            self.card_list.append(Card.Card(i, "spades"))
        for i in range(9,15):
            self.card_list.append(Card.Card(i, "hearts"))

    def test_is_leading(self): # if the suit lead of the trick is None then all cards are valid, no need to check anything about a hand
        for card in self.card_list:
            self.assertTrue(self.test_tree.validate(card, self.temp_player, self.temp_round))

    def test_can_follow_suit(self): # if this player can follow suit, only cards of that suit are valid
        self.temp_trick.accept(self.card_list[15]) # put the Ace of Clubs on the trick
        for i in range(16,25): # give the player 8 cards: 10C, KC, 9C, 8C, 7C, AS, 10S, KS
            self.temp_player.accept(self.card_list[i])
        for i in range(self.temp_player.hand.card_list.size()):
            if i < 6: # the first 5 cards in the players hand are clubs and should be valid to play
                self.assertTrue(self.test_tree.validate(self.temp_player.hand.card_list[i], self.temp_player, self.temp_round))
            else: # all remaining cards in the players hand are spades and should not be valid to play
                self.assertFalse(self.test_tree.validate(self.temp_player.hand.card_list[i], self.temp_player, self.temp_round))

    def test_cannot_follow_suit_has_trump(self): # if this player cannot follow suit and has trump, only trump cards are valid
        self.temp_trick.accept(self.card_list[31]) # put the 7H on the trick
        for i in range(11,19): # give 8 cards to the player: KD, 9D, 8D, AC, 10C, KC, 9C, 8C
            self.temp_player.accept(self.card_list[i])
        for i in range(self.temp_player.hand.card_list.size()):
            if i < 4: # the first 3 cards in the players hand are trump and should be playable
                self.assertTrue(self.test_tree.validate(self.temp_player.hand.card_list[i], self.temp_player, self.temp_round))
            else: # all remaining cards in the players hand are not trump or the suit lead and should not be playable
                self.assertFalse(self.test_tree.validate(self.temp_player.hand.card_list[i], self.temp_player, self.temp_round))

    def test_cannot_follow_suit_has_no_trump(self): # if this player cannot follow suit and has no trump, then all cards in hand are valid
        self.temp_trick.accept(self.card_list[31]) # put the 7H on the trick
        for i in range(16,24): # give the player 8 cards: 10C, KC, 9C, 8C, 7C, AS, 10S, KS
            self.temp_player.accept(self.card_list[i])
        for i in range(self.temp_player.hand.card_list.size()):
            self.assertTrue(self.test_tree.validate(self.temp_player.hand.card_list[i], self.temp_player, self.temp_round))

    def test_ace_called_and_player_has_called_ace_with_suit_lead(self): # if this player has the ace that was called and that suit was lead, only that ace is a valid card
        self.temp_round.call_matrix[1][4] = 1 # force the round to have the second player have called the ace of hearts
        self.temp_trick.accept(self.card_list[31]) # put the 7H on the trick
        for i in range(22,30): # give the player 8 cards: KS,9S,8S,7S,AH,10H,KH,9H
            self.temp_player.accept(self.card_list[i])
        for i in range(self.temp_player.hand.card_list.size()):
            if i != 4:
                self.assertFalse(self.test_tree.validate(self.temp_player.hand.card_list[i], self.temp_player, self.temp_round))
            else: # since the player has the ace and that suit was lead only that ace is a valid card to play
                self.assertTrue(self.test_tree.validate(self.temp_player.hand.card_list[i], self.temp_player, self.temp_round))

    def test_ace_called_and_player_has_called_ace_with_suit_not_lead(self): # if this player has the ace that was called and that suit was not lead, then that ace is not a valid card to play
        self.temp_round.call_matrix[1][4] = 1 # force the round to have the second player have called the ace of hearts
        self.temp_trick.accept(self.card_list[14]) # put the AC on the trick
        for i in range(22,30): # give the player 8 cards: KS,9S,8S,7S,AH,10H,KH,9H
            self.temp_player.accept(self.card_list[i])
        for i in range(self.temp_player.hand.card_list.size()):
            if i == 4: # since the player has the ace called and that suit was not lead that ace is not a valid card to play
                self.assertFalse(self.test_tree.validate(self.temp_player.hand.card_list[i], self.temp_player, self.temp_round))
            else: # all other cards are valid here since this player doesn't have trump or the suit lead
                self.assertTrue(self.test_tree.validate(self.temp_player.hand.card_list[i], self.temp_player, self.temp_round))

    def tearDown(self):
        for card in self.card_list:
            del card
        del self.card_list
        del self.test_tree

#             index 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 ,10, 11,12,13,14,15,16,17,18,19, 20,21,22,23,24,25, 26,27,28,29,30,31
#32 cards in order: QC,7D,QS,QH,QD,JC,JS,JH,JD,AD,10D,KD,9D,8D,(A,10,K ,9 ,8 ,7)C,(A,10,K ,9 ,8 ,7)S,(A,10,K ,9 ,8 ,7)H
#              rank 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11,12,13, 9,10,11,12,13,14,  9,10,11,12,13,14,  9,10,11,12,13,14
if __name__ == "__main__":
    unittest.main()