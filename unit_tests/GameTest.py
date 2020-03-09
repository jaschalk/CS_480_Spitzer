import unittest
from unit_tests.Setup import general_setup
from game_objects.Deck import Deck
from game_objects.CallRules import CallRules
from game_objects.CardRuleTree import CardRuleTree
from game_objects.PartnerRuleTree import PartnerRuleTree

#Need to hash out the wins and tie methods before actually testing this. Or do we even need these methods anymore?

class GameTest(unittest.TestCase):

    def setUp(self):
        setup_results = general_setup()
        self.temp_game = setup_results["active_game"]
        self.temp_deck = setup_results["game_deck"]
        self.temp_player_list = setup_results["list_of_players"]
        self.temp_round = setup_results["current_round"]
        del setup_results

    def test_on_init(self):
        self.assertEqual(len(self.temp_player_list), 4)
        self.assertIsInstance(self.temp_deck, Deck)
        #self.assertEqual(self.testGame.listOfRounds.size(), 0) #The game no longer keeps track of a list of rounds
        self.assertIsInstance(self.temp_game.get_card_rules(), CardRuleTree)
        self.assertIsInstance(self.temp_game.get_partner_rules(), PartnerRuleTree)
        self.assertIsInstance(self.temp_game.get_call_rules(), CallRules)

    def test_deal_cards(self):
        temp_player = self.temp_player_list[0]
        self.temp_deck.deal_cards_to(temp_player)
        self.assertEqual((self.temp_deck + len(temp_player.get_cards_in_hand())), 32)

    def test_end_game_one_winner(self):
        self.temp_player_list[0].set_total_score(42)
        self.temp_player_list[1].set_total_score(30)
        self.temp_player_list[2].set_total_score(28)
        self.temp_player_list[3].set_total_score(20)
        self.assertTrue(self.temp_player_list[0].wins()) #Have this method return a boolean on whether or not the asking player wins.

    def test_end_game_tie(self):
        self.temp_player_list[0].set_total_score(42)
        self.temp_player_list[1].set_total_score(42)
        self.temp_player_list[2].set_total_score(28)
        self.temp_player_list[3].set_total_score(20)
        self.assertTrue(self.temp_player_list[0].tie(self.temp_player_list[1])) #Have this method return a boolean on whether or not the asking player ties with the argument player

    def test_end_game_continues(self):
        self.temp_player_list[0].set_total_score(36)
        self.temp_player_list[1].set_total_score(30)
        self.temp_player_list[2].set_total_score(28)
        self.temp_player_list[3].set_total_score(20)
        for index in range(4):
            self.assertFalse(self.temp_player_list[index].wins())

    def tearDown(self):
        del self.temp_game
        del self.temp_deck
        del self.temp_player_list
        del self.temp_round


if __name__ == "__main__":
    unittest.main()