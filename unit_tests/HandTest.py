import unittest
from game_objects.Hand import Hand
from game_objects.Deck import Deck
from game_objects.Trick import Trick
from game_objects.Player import Player
from game_objects.Round import Round
from game_objects.Game import Game
import agents

class HandTest(unittest.TestCase):

    def setUp(self):
        self.temp_agents = [0, 0, 0, 0]
        self.temp_game = Game(0, self.temp_agents)
        self.temp_deck = Deck()
        self.temp_player = Player(self.temp_game, 0, None)
        self.temp_round = Round(self.temp_game) #Can't pass in None here.
        self.temp_game._round = self.temp_round
        self.test_hand = Hand(self.temp_player)

    def test_on_init(self):
        self.assertEqual(len(self.test_hand.get_cards_in_hand()), 0)
        for entry in self.test_hand._valid_play_list:
            self.assertTrue(entry)

    def test_on_deal(self):
        self.temp_player.hand = self.test_hand
        self.temp_deck.deal_cards_to(self.temp_player)
        self.assertEqual(len(self.test_hand.get_cards_in_hand()), 8)

    def test_card_played(self):
        self.temp_round.set_leading_player(self.temp_player)
        self.temp_deck.deal_cards_to(self.temp_player)
        self.temp_trick = Trick(self.temp_round)
        #self.temp_round.set_current_trick(self.temp_trick)
        startHandSize = len(self.test_hand.get_cards_in_hand())

        startValidListSize = len(self.test_hand.get_valid_play_list())
        self.test_hand.play_card_at_index(self.temp_trick, 0)
        self.assertEqual(len(self.test_hand.get_cards_in_hand()), startHandSize - 1)
        for card in self.test_hand.get_cards_in_hand():
            print(card)
        self.test_hand.determine_valid_play_list()
        self.assertEqual(len(self.test_hand.get_valid_play_list()), startValidListSize - 1)


    def tearDown(self):
        self.test_hand.get_cards_in_hand().clear()
        del self.test_hand

if __name__ == "__main__":
    unittest.main()