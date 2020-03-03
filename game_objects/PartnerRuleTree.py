from game_objects import RuleNode

#IMPORTANT: I don't think I am returning any strings at all. Meaning, when I try to see if the
#           string returned is "target is my partner", "target is not my partner", and "unknown"
#           I'm not actually returning any strings to check against. Where would I do this??

class PartnerRuleTree:

    _root = None

    def get_root(self):
        return self._root

    def __init__(self):

        #args should be aPlayer, aPlayer, and aRound in that order.
        
        def get_ace_called_id(*args):
            # need to go through the call matrix to see what ace was called
            call_state = args[2].get_call_matrix()
            which_call = -1
            for call_num in range (1,4):
                for player_num in range(4):
                    if(call_state[player_num][call_num] == 1):
                        which_call = call_num
                        break
            # the ace will be card # 14 + 6*(call_index - 1)
            return 14 + 6*(which_call - 1)

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
            asking_player_id = args[0].get_player_id
            call_matrix = args[2].get_call_matrix()
            asking_player_made_call = False
            for index in range(1, 8):
                if (call_matrix[index][asking_player_id] == 1):
                    asking_player_made_call = True
            return asking_player_made_call

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
            cards_in_player_hand_binary_state = args[0].get_hand().get_binary_representation()
            cards_asking_has_played = args[2].get_player_binary_card_state(args[0].get_player_id())
            return ((cards_asking_has_played + cards_in_player_hand_binary_state) & 1<<ace_called == 1<<ace_called)

        def has_ace_been_played(*args):
            trick_history = args[2].get_trick_history()
            ace_called = get_ace_called_id(*args)
            ace_has_been_played = False
            for index in range(4):
                for i in range(8):
                    if(trick_history[index][i][ace_called] == 1):
                        ace_has_been_played = True
            return ace_has_been_played

        def does_asking_player_have_a_queen(*args):
            player_hand_binary_representation = args[0].get_hand().get_binary_representation()
            cards_asking_has_played = args[2].get_player_binary_card_state(args[0].get_player_id())
            return ((player_hand_binary_representation + cards_asking_has_played) & 0b1 == 0b1) or ((player_hand_binary_representation + cards_asking_has_played) & 0b100 == 0b100)

        def does_asking_player_have_both_queens(*args):
            #Maybe make a method to take care of the first two lines and return the number.
            player_hand_binary_representation = args[0].get_hand().get_binary_representation()
            cards_asking_has_played = args[2].get_player_binary_card_state(args[0].get_player_id())
            return ((player_hand_binary_representation + cards_asking_has_played) & 0b101 == 0b101)

        def does_target_player_have_a_queen(*args):
            cards_target_has_played = args[2].get_player_binary_card_state(args[1].get_player_id())
            return ((cards_target_has_played & 0b1 == 0b1) or (cards_target_has_played & 0b100 == 0b100))

        def have_both_queens_been_played(*args): 
            cards_played = args[2].get_cards_played()
            return (cards_played & 0b101 == 0b101)

        self._root = RuleNode.RuleNode(self, "Returns true if a call has been made.", has_call_been_made)
        __root_R = RuleNode.RuleNode(self, "Returns true if the asking player has a queen.", does_asking_player_have_a_queen)
        __root_RL = RuleNode.RuleNode(self, "Returns true if the asking player has both queens.", does_asking_player_have_both_queens)
        __root_RLR = RuleNode.RuleNode(self, "Returns true if the target player has a queen.", does_target_player_have_a_queen)
        __root_RLRR = RuleNode.RuleNode(self, "Returns true if both queens have been played.", have_both_queens_been_played)
        __root_RR = RuleNode.RuleNode(self, "Returns true if the target player has a queen", does_target_player_have_a_queen)
        __root_RRR = RuleNode.RuleNode(self, "Returns true if both queens have been played", have_both_queens_been_played)
        __root_L = RuleNode.RuleNode(self, "Returns true if the asking player made the call.", did_asking_player_make_call)
        __root_LL = RuleNode.RuleNode(self, "Returns true if the call made was for first trick.", was_first_trick_called)
        __root_LLL = RuleNode.RuleNode(self, "Returns true if the target player took the first trick.", did_target_take_first_trick)
        __root_LLR = RuleNode.RuleNode(self, "Returns true if the call made was for an ace.", was_ace_called)
        __root_LLRL = RuleNode.RuleNode(self, "Returns true if the target player has the ace called", does_target_player_have_ace)
        __root_LLRLR = RuleNode.RuleNode(self, "Returns true if the ace called has been played.", has_ace_been_played)
        __root_LR = RuleNode.RuleNode(self, "Returns true if the call made was for first trick.", was_first_trick_called)
        __root_LRL = RuleNode.RuleNode(self, "Returns true if the asking player took the first trick.", did_asking_take_first_trick)
        __root_LRR = RuleNode.RuleNode(self, "Returns true if the call made was for an ace.", was_ace_called)
        __root_LRRL = RuleNode.RuleNode(self, "Returns true if the asking player has the ace called.", does_asking_player_have_ace)
        __root_LRRLR = RuleNode.RuleNode(self, "Returns true if the ace called has been played.", has_ace_been_played)
        self._root.set_right(__root_R)
        self._root.set_left(__root_L)
        __root_R.set_right(__root_RR)
        __root_R.set_left(__root_RL)
        __root_RR.set_right(__root_RRR)
        __root_RL.set_right(__root_RLR)
        __root_RLR.set_right(__root_RLRR)
        __root_L.set_right(__root_LR)
        __root_LR.set_right(__root_LRR)
        __root_LR.set_left(__root_LRL)
        __root_LRR.set_left(__root_LRRL)
        __root_LRRL.set_right(__root_LRRLR)
        __root_L.set_left(__root_LL)
        __root_LL.set_left(__root_LLL)
        __root_LL.set_right(__root_LLR)
        __root_LLR.set_left(__root_LLRL)
        __root_LLRL.set_right(__root_LLRLR) 

    def validate_partners(self, asking_player, target_player, a_round):
        _result = self._root.validate(asking_player, target_player, a_round)
        if _result == True:
            return "target is my partner"
        elif _result == False:
            return "target is not my partner"
        else:
            return "unknown"     