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

        def did_asking_player_make_call(*args):

        def was_first_trick_called(*args):
            call_state = args[2].get_call_matrix()
            first_trick_called = False
            for i in range(4): #query each players index in the call matrix to see if they called an ace
                if(call_state[i][4] == 1):
                    first_trick_called = True
            return first_trick_called

        def was_ace_called(*args):
            call_state = args[2].get_call_matrix()
            ace_called = False
            for i in range(4): #query each players index in the call matrix to see if they called an ace
                if(call_state[i][1] == 1 or call_state[i][2] == 1 or call_state[i][3] == 1):
                    ace_called = True
            return ace_called

        def was_solo_called(*args):
            call_state = args[2].get_call_matrix()
            solo_called = False
            for i in range(4): #query each players index in the call matrix to see if they called an ace
                if(call_state[i][5] == 1 or call_state[i][6] == 1 or call_state[i][7] == 1):
                    solo_called = True
            return solo_called

        def does_asking_player_have_a_queen(*args):

        def does_target_player_have_a_queen(*args):

        def have_both_black_queens_been_played(*args):  