from game_objects.Game import Game
import agents

def general_setup():
    '''
    Returns a dictonary that contains all the necessary objects for testing purposes linked together in the proper ways.
    
    Valid keys are: active_game, game_deck, list_of_players, current_round, player_zero_hand, current_trick, call_rules, card_rules, partner_rules
    '''
    list_of_agents = [None, None, None, None]
    active_game = Game(0, list_of_agents)
    active_game._supress_write_to_winners_log = True
    game_deck = active_game.get_deck()
    list_of_players = []
    for i in range(4):
        list_of_players.append(active_game.get_players_list()[i])
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