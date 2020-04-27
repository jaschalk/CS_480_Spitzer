
import random
import operator

class RandomAgent:

    call_weight_list = [1200, 2400, 2400, 2400, 3600, 150, 10, 1] #NC, AC, AS, AH, FT, Z, ZS, ZSS

    def make_call(self, a_player):
        call_list_after_weight = list(map(operator.mul, a_player.get_valid_call_list(), self.call_weight_list))
        total = 0
        for index in range(8):
            total += call_list_after_weight[index]
        for index in range(8):
            call_list_after_weight[index] = (call_list_after_weight[index]/total)
            if index != 0:
                call_list_after_weight[index] = call_list_after_weight[index] + call_list_after_weight[index-1]
        call_to_make = random.random()
        for index in range(8):
            if call_to_make <= call_list_after_weight[index]:
                return index
        raise RuntimeError("Returned an invalid index")

    def play_card(self, a_player, a_game):
        valid_indices = [index for index in range(len(a_player.get_valid_play_list())) if a_player.get_valid_play_list()[index] != 0]
        if len(valid_indices) == 1: 
            return valid_indices[0]
        temp = valid_indices[random.randint(0,len(valid_indices)-1)]
        return temp