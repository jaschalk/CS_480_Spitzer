from game_objects import RuleNode

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
            #where are we keeping track of this info? Are we keeping track of this info?
            pass

        def has_call_been_made(*args):
            call_has_been_made = False
            call_matrix = call_matrix = args[2].get_call_matrix()
            for index in range(4):
                for i in range(8):
                    if(call_matrix[index][i] == 1):
                        call_has_been_made = True
            return call_has_been_made
        
        def did_asking_player_make_call(*args):
            asking_player_id = args[0].get_player_id
            call_matrix = args[2].get_call_matrix()
            asking_player_made_call = False
            for index in range(8):
                if (call_matrix[index][asking_player_id] == 1):
                    asking_player_made_call = True
            return asking_player_made_call

        def was_first_trick_called(*args):
            call_state = args[2].get_call_matrix()
            first_trick_called = False
            for i in range(4): #query each players index in the call matrix to see if they called an ace
                if(call_state[i][4] == 1):
                    first_trick_called = True
            return first_trick_called

        def did_target_take_first_trick(*args):
            took_first_trick = get_player_took_first_trick(*args)
            target_player_id = args[1].get_player_id()
            if(took_first_trick == target_player_id):
                return True
            else:
                return False

        def did_asking_take_first_trick(*args): #Repeated code. Is this what we want here?
            took_first_trick = get_player_took_first_trick(*args)
            asking_player_id = args[0].get_player_id()
            if(took_first_trick == asking_player_id):
                return True
            else:
                return False

        def was_ace_called(*args):
            call_state = args[2].get_call_matrix()
            ace_was_called = False
            for i in range(4): #query each players index in the call matrix to see if they called an ace
                if(call_state[i][1] == 1 or call_state[i][2] == 1 or call_state[i][3] == 1):
                    ace_was_called = True
            return ace_was_called

        def does_target_player_have_ace(*args):
            ace_called = get_ace_called_id(*args)
            cards_in_player_hand = args[1].get_hand().get_cards_in_hand()
            target_player_has_ace = False
            for index in range(cards_in_player_hand.size):
                if(cards_in_player_hand[index] == ace_called):
                    target_player_has_ace = True
            return target_player_has_ace

        def does_asking_player_have_ace(*args): #repeated code. Is this what we want here?
            ace_called = get_ace_called_id(*args)
            cards_in_player_hand = args[0].get_hand().get_cards_in_hand()
            asking_player_has_ace = False
            for index in range(cards_in_player_hand.size):
                if(cards_in_player_hand[index] == ace_called):
                    asking_player_has_ace = True
            return asking_player_has_ace

        def has_ace_been_played(*args):
            trick_history = args[2].get_trick_history
            ace_called = get_ace_called_id #I don't think this number is what I want it to be. Need some clarification.
            ace_has_been_played = False
            for index in range(4):
                for i in range(8):
                    if(trick_history[index][i][ace_called] == 1):
                        ace_has_been_played = True
            return ace_has_been_played

        def was_solo_called(*args):
            call_state = args[2].get_call_matrix()
            solo_called = False
            for i in range(4): #query each players index in the call matrix to see if they called an ace
                if(call_state[i][5] == 1 or call_state[i][6] == 1 or call_state[i][7] == 1):
                    solo_called = True
            return solo_called

        def does_asking_player_have_a_queen(*args):
            cards_in_player_hand = args[0].get_hand().get_cards_in_hand()
            asking_player_queen = False
            for index in range(8):
                if(cards_in_player_hand[index].get_card_id() == 0 or cards_in_player_hand[index].get_card_id() == 2):
                    asking_player_queen = True
            return asking_player_queen

        def does_asking_player_have_both_queens(*args):
            cards_in_player_hand = args[0].get_hand().get_cards_in_hand()
            asking_player_first_queen = False
            asking_player_second_queen = False
            for index in range(8):
                if(cards_in_player_hand[index].get_card_id() == 0):
                    asking_player_first_queen = True
                elif(cards_in_player_hand[index].get_card_id() == 2):
                    asking_player_second_queen = True
            if(asking_player_first_queen and asking_player_second_queen):
                return True
            else:
                return False

        def does_target_player_have_a_queen(*args): #repeated code here. Can we simplify? Also still getting confused on have vs play. Is this what we want here?
            cards_in_player_hand = args[1].get_hand().get_cards_in_hand()
            target_player_queen = False
            for index in range(8):
                if(cards_in_player_hand[index].get_card_id() == 0 or cards_in_player_hand[index].get_card_id() == 2):
                    target_player_queen = True
            return target_player_queen

        def have_both_queens_been_played(*args): 
            trick_history = args[2].get_trick_history()
            both_queens_played = False
            for index in range(8): #in each trick...
                for i in range(4): #for every player...
                    if(trick_history[i][index][0] == 1 or trick_history[i][index][2] == 1):
                        both_queens_played = True
            return both_queens_played

        self._root = RuleNode.RuleNode(self, "Returns true if a call has been made.", has_call_been_made)
        __root_R = RuleNode.RuleNode(self, "Returns true if the asking player has a queen.", does_asking_player_have_a_queen)
        __root_RL = RuleNode.RuleNode(self, "Returns true if the asking player has both queens.", does_asking_player_have_both_queens)
        __root_RLR = RuleNode.RuleNode(self, "Returns true if the target player has a queen.", does_target_player_have_a_queen)
        __root_RLRR = RuleNode.RuleNode(self, "Returns true if both queens have been played.", have_both_queens_been_played)
        __root_RR = RuleNode.RuleNode(self, "Returns true if the target player has a queen", does_target_player_have_a_queen)
        __root_RRR = RuleNode.RuleNode(self, "Returns true if both queens have been played", have_both_queens_been_played)
        __root_RRR = RuleNode.RuleNode(self, "Returns true if the asking player has trump cards.", does_player_have_trump)
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
        __root_L.set_right(__root._LR)
        __root._LR.set_right(__root._LRR)
        __root._LR.set_left(__root._LRL)
        __root._LRR.set_left(__root._LRRL)
        __root._LRRL.set_right(__root._LRRLR)
        __root_L.set_left(__root._LL)
        __root._LL.set_left(__root._LLL)
        __root._LL.set_right(__root.LLR)
        __root._LLR.set_left(__root._LLRL)
        __root.LLRL.set_right(__root._LLRLR) 

        def validate_partners(self, asking_player, target_player, a_round):
            self._root.validate(asking_player, target_player, a_round)     