from game_objects.Game import Game
from game_objects.Deck import Deck
from game_objects.Round import Round
from game_objects.Trick import Trick
from game_objects.Player import Player
from game_objects.Hand import Hand
from game_objects.Card import Card
from game_objects.CallRules import CallRules
from game_objects.CardRuleTree import CardRuleTree
from game_objects.PartnerRuleTree import PartnerRuleTree
import agents

def general_setup():
    '''
    Returns a dictonary that contains all the necessary objects for testing purposes linked together in the proper ways.
    
    Valid keys are: active_game, game_deck, list_of_players, current_round, player_zero_hand, current_trick, call_rules, card_rules, partner_rules
    '''
    list_of_agents = [None, None, None, None]
    active_game = Game(0, list_of_agents)
    game_deck = active_game.get_deck()
    list_of_players = []
    for i in range(4):
        list_of_players.append(Player(active_game, i, list_of_agents[i]))
    current_round = active_game.get_round()
    player_zero_hand = list_of_players[0].get_hand()
    current_trick = current_round.get_current_trick()
    call_rules = active_game.get_call_rules()
    card_rules = active_game.get_card_rules()
    partner_rules = active_game.get_partner_rules()
    output = {"active_game":active_game,
                "game_deck":game_deck,
                "list_of_players":list_of_players,
                "current_round":current_round,
                "player_zero_hand":player_zero_hand,
                "current_trick": current_trick,
                "call_rules":call_rules,
                "card_rules":card_rules,
                "partner_rules":partner_rules}
    return output