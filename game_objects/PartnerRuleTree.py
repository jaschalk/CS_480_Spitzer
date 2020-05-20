from game_objects.RuleNode import RuleNode
from game_objects.RuleNodeUnknown import RuleNodeUnknown
from game_objects.RuleNodeFalse import RuleNodeFalse
from game_objects.RuleNodeTrue import RuleNodeTrue
from enums import CardBinary
import RuleTreeFunctions as rtf

class PartnerRuleTree:
    '''
    The Partner Rule Tree class is used to determine whether or not a player
    should update their potential partners list.
    '''

    _root = None

    def get_root(self):
        return self._root

    def __init__(self):

        #args should be aPlayer, aPlayer, and aRound in that order.

        both_queens_value = CardBinary.queen_clubs.value + CardBinary.queen_spades.value

        def get_ace_called_id(*args):
            # this assumes that an ace has been called
            # need to go through the call matrix to see what ace was called
            call_state = args[2].get_call_matrix()
            which_call = -1
            for call_num in range (1,4):
                for player_num in range(4):
                    if(call_state[player_num][call_num] == 1):
                        which_call = call_num
                        break
            return 14 + 6*(which_call - 1)#This will be the id number of the ace that was called

        def get_player_took_first_trick(*args):
            return args[2].get_first_trick_winner().get_player_id()

        def has_call_been_made(*args):
            call_has_been_made = False
            call_matrix = args[2].get_call_matrix()
            for index in range(4):
                for i in range(1, 8):
                    if(call_matrix[index][i] == 1):
                        call_has_been_made = True
            return call_has_been_made

        def did_asking_player_make_call(*args):
            asking_player_id = args[0].get_player_id()
            call_matrix = args[2].get_call_matrix()
            asking_player_made_call = False
            for index in range(1, 8):
                if (call_matrix[asking_player_id][index] == 1):
                    asking_player_made_call = True
            return asking_player_made_call

        def did_target_player_make_call(*args):
            target_player_id = args[1].get_player_id()
            call_matrix = args[2].get_call_matrix()
            target_player_made_call = False
            for index in range(1, 8):
                if(call_matrix[target_player_id][index] == 1):
                    target_player_made_call = True
            return target_player_made_call

        def was_first_trick_called(*args):
            call_state = args[2].get_call_matrix()
            first_trick_called = False
            for i in range(4): #query each players index in the call matrix to see if they called first trick
                if(call_state[i][4] == 1):
                    first_trick_called = True
            return first_trick_called

        def did_target_take_first_trick(*args):
            return get_player_took_first_trick(*args) == args[1].get_player_id()

        def did_asking_take_first_trick(*args):
            return get_player_took_first_trick(*args) == args[0].get_player_id()

        def was_ace_called(*args):
            call_state = args[2].get_call_matrix()
            ace_was_called = False
            for i in range(4): #query each players index in the call matrix to see if they called an ace
                if(call_state[i][1] == 1 or call_state[i][2] == 1 or call_state[i][3] == 1):
                    ace_was_called = True
            return ace_was_called

        def does_target_player_have_ace(*args):
            ace_called = get_ace_called_id(*args)
            cards_target_has_played = args[2].get_player_binary_card_state(args[1].get_player_id())
            return (cards_target_has_played & 1<<ace_called == 1<<ace_called)

        def does_asking_player_have_ace(*args):
            ace_called = get_ace_called_id(*args)
            cards_in_player_hand_binary_state = args[0].get_hand_binary_representation()
            cards_asking_has_played = args[2].get_player_binary_card_state(args[0].get_player_id())
            return ((cards_asking_has_played + cards_in_player_hand_binary_state) & 1<<ace_called == 1<<ace_called)

        def has_ace_been_played(*args):
            #Two options can be returned here: target is not my partner or unknown
            trick_history = args[2].get_trick_history()
            ace_called = get_ace_called_id(*args)
            ace_has_been_played = False
            for index in range(4):
                for i in range(8):
                    if(trick_history[index][i][ace_called] == 1):
                        ace_has_been_played = True
            return ace_has_been_played

        def did_target_play_ace(*args):
            target_cards_played = args[1].get_cards_played()
            ace_called = get_ace_called_id(*args)
            return target_cards_played & 1<<ace_called

        def does_asking_player_have_a_queen(*args):
            player_hand_binary_representation = args[0].get_hand_binary_representation()
            cards_asking_has_played = args[2].get_player_binary_card_state(args[0].get_player_id())
            return ((player_hand_binary_representation + cards_asking_has_played) & CardBinary.queen_clubs.value == CardBinary.queen_clubs.value) or ((player_hand_binary_representation + cards_asking_has_played) & CardBinary.queen_spades.value == CardBinary.queen_spades.value)

        def does_asking_player_have_both_queens(*args):
            player_hand_binary_representation = args[0].get_hand_binary_representation()
            cards_asking_has_played = args[2].get_player_binary_card_state(args[0].get_player_id())
            return ((player_hand_binary_representation + cards_asking_has_played) & both_queens_value == both_queens_value)

        def does_target_player_have_a_queen(*args):
            cards_target_has_played = args[2].get_player_binary_card_state(args[1].get_player_id())
            return ((cards_target_has_played & CardBinary.queen_clubs.value == CardBinary.queen_clubs.value) or (cards_target_has_played & CardBinary.queen_spades.value == CardBinary.queen_spades.value))

        def did_asking_player_play_a_queen(*args):
            cards_asking_has_played = args[2].get_player_binary_card_state(args[0].get_player_id())
            return ((cards_asking_has_played & CardBinary.queen_clubs.value == CardBinary.queen_clubs.value) or (cards_asking_has_played & CardBinary.queen_spades.value == CardBinary.queen_spades.value))

        def have_both_queens_been_played(*args):
            cards_played = args[2].get_cards_played()
            return (cards_played & both_queens_value == both_queens_value)

        def has_one_queen_been_played(*args):
            cards_played = args[2].get_cards_played()
            return (cards_played & CardBinary.queen_clubs.value == CardBinary.queen_clubs.value or cards_played & CardBinary.queen_spades.value == CardBinary.queen_spades.value)

        self._root = RuleNode("Returns true if a call has been made.", has_call_been_made)
        __root_R = RuleNode("Returns true if the asking player has a queen.", does_asking_player_have_a_queen)
        __root_RL = RuleNode("Returns true if the asking player has both queens.", does_asking_player_have_both_queens)
        __root_RLR = RuleNode("Returns true if the target player has a queen.", does_target_player_have_a_queen)
        __root_RLRR = RuleNode("Returns true if both queens have been played.", have_both_queens_been_played)
        __root_RLRRR = RuleNode("Returns true one queen has been played.", has_one_queen_been_played)
        __root_RLRRRL = RuleNode("Returns true if the target player has played a queen.", does_target_player_have_a_queen)
        __root_RLRRRLR = RuleNode("Returns true if the asking player has played a queen.", did_asking_player_play_a_queen)
        __root_RR = RuleNode("Returns true if the target player has a queen", does_target_player_have_a_queen)
        __root_RRR = RuleNode("Returns true if both queens have been played", have_both_queens_been_played)
        __root_L = RuleNode("Returns true if the asking player made the call.", did_asking_player_make_call)
        __root_LL = RuleNode("Returns true if the call made was for first trick.", was_first_trick_called)
        __root_LLL = RuleNode("Returns true if the target player took the first trick.", did_target_take_first_trick)
        __root_LLR = RuleNode("Returns true if the call made was for an ace.", was_ace_called)
        __root_LLRL = RuleNode("Returns true if the target player has the ace called", does_target_player_have_ace)
        __root_LLRLR = RuleNode("Returns true if the ace called has been played.", has_ace_been_played)
        __root_LR = RuleNode("Returns true if the target player made the call.", did_target_player_make_call)
        __root_LRL = RuleNode("Returns true if the call made was for first trick.", was_first_trick_called)
        __root_LRLL = RuleNode("Returns true if the asking player took the first trick.", did_asking_take_first_trick)
        __root_LRLR = RuleNode("Returns true if the call made was for an ace.", was_ace_called)
        __root_LRLRL = RuleNode("Returns true if the asking player has the ace called.", does_asking_player_have_ace)
        __root_LRLRLR = RuleNode("Returns true if the ace called has been played.", has_ace_been_played)
        __root_LRR = RuleNode("Returns true if the call made was for first trick.", was_first_trick_called)
        __root_LRRL = RuleNode("Returns true if the asking player took the first trick.", did_asking_take_first_trick)
        __root_LRRLR = RuleNode("Returns true if the target player took the first trick.", did_target_take_first_trick)
        __root_LRRR = RuleNode("Returns true if the call made was for an ace.", was_ace_called)
        __root_LRRRL = RuleNode("Returns true if the asking player has the ace called.", does_asking_player_have_ace)
        __root_LRRRLR = RuleNode("Returns true if the ace called has been played.", has_ace_been_played)
        __root_LRRRLRL = RuleNode("Returns true if the target player played the ace called.", did_target_play_ace)
        self._root.set_right(__root_R)
        self._root.set_left(__root_L)
        __root_R.set_right(__root_RR)
        __root_R.set_left(__root_RL)
        __root_RR.set_right(__root_RRR)
        __root_RR.set_left(RuleNodeFalse())
        __root_RRR.set_right(RuleNodeUnknown())
        __root_RL.set_right(__root_RLR)
        __root_RL.set_left(RuleNodeFalse())
        __root_RLR.set_right(__root_RLRR)
        __root_RLRR.set_left(RuleNodeFalse())
        __root_RLRR.set_right(__root_RLRRR)
        __root_RLRRR.set_left(__root_RLRRRL)
        __root_RLRRR.set_right(RuleNodeUnknown())
        __root_RLRRRL.set_right(__root_RLRRRLR)
        __root_RLRRRLR.set_left(RuleNodeUnknown())
        __root_L.set_right(__root_LR)
        __root_LR.set_right(__root_LRR)
        __root_LRR.set_left(__root_LRRL)
        __root_LRR.set_right(__root_LRRR)
        __root_LRRL.set_left(RuleNodeFalse())
        __root_LRRL.set_right(__root_LRRLR)
        __root_LRRLR.set_left(RuleNodeFalse())
        __root_LRRLR.set_right(RuleNodeTrue())
        __root_LRRR.set_left(__root_LRRRL)
        __root_LRRR.set_right(RuleNodeTrue())
        __root_LRRRL.set_left(RuleNodeFalse())
        __root_LRRRL.set_right(__root_LRRRLR)
        __root_LRRRLR.set_left(__root_LRRRLRL)
        __root_LRRRLR.set_right(RuleNodeUnknown())
        __root_LRRRLRL.set_left(RuleNodeFalse())
        __root_LRRRLRL.set_right(RuleNodeTrue())
        __root_LR.set_left(__root_LRL)
        __root_LRL.set_left(__root_LRLL)
        __root_LRL.set_right(__root_LRLR)
        __root_LRLR.set_left(__root_LRLRL)
        __root_LRLRL.set_right(__root_LRLRLR)
        __root_LRLRLR.set_right(RuleNodeUnknown())
        __root_LRLRLR.set_left(RuleNodeFalse())
        __root_L.set_left(__root_LL)
        __root_LL.set_left(__root_LLL)
        __root_LL.set_right(__root_LLR)
        __root_LLR.set_left(__root_LLRL)
        __root_LLRL.set_right(__root_LLRLR)
        __root_LLRLR.set_right(RuleNodeUnknown())
        __root_LLRLR.set_left(RuleNodeFalse())

    def validate_partners(self, asking_player, target_player, a_round):
        _result = self._root.validate(asking_player, target_player, a_round)
        if _result == True:
            return "target is my partner"
        elif _result == False:
            return "target is not my partner"
        else:
            return "unknown"