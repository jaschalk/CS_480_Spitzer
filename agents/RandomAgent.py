
import random
import operator

class RandomAgent:

    call_weight_list = [700, 1400, 1400, 1400, 2100, 150, 10, 1] #NC, AC, AS, AH, FT, Z, ZS, ZSS # TODO Change numbers back to something sensible
    
    def make_call(self, a_player):
        #Should return the index in the call list of the call the agent "chooses" to make.
        #In this case, the index returned is generated by creating a cumulative probability distribution
        #and generating a random number between 0 and 1 and choosing the call index that corresponds
        #to the range the generated number falls in. Return -1 on error
        #See back of call rule paper for example.
        call_list_after_weight = list(map(operator.mul, a_player.get_valid_call_list(), self.call_weight_list))
        total = 0
        for index in range(8):
            total += call_list_after_weight[index]
        for index in range(8):
            call_list_after_weight[index] = (call_list_after_weight[index]/total)
            if index != 0:
                call_list_after_weight[index] = call_list_after_weight[index] + call_list_after_weight[index-1]
        call_to_make = random.random() #generate a random floating pt. number between 0 and 1
        for index in range(8):
            if call_to_make <= call_list_after_weight[index]:
                return index
        raise RuntimeError("Returned an invalid index")

    def play_card(self, a_player, a_game):
        #Should return the index in the valid play list of the card the agent "chooses" to play.
        #In this case, the index returned is a random number between 0 and the length of the valid play list.
        valid_indices = [index for index in range(len(a_player.get_valid_play_list())) if a_player.get_valid_play_list()[index] != 0]
        if len(valid_indices) == 1:
            return 0
        temp = valid_indices[random.randint(0,len(valid_indices)-1)]
        return temp