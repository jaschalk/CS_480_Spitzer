from agents.agent import Agent
import random
import operator

class RandomAgent(Agent):

    call_weight_list = [700, 900, 900, 900, 1000, 150, 10, 1] #NC, AC, AS, AH, FT, Z, ZS, ZSS
    
    def make_call(self, a_player):
        #Should return the index in the call list of the call the agent "chooses" to make.
        #In this case, the index returned is generated by creating a ??? and generating a random number between 0 and 1
        #and choosing the call index that corresponds to the range the generated number falls in.
        #return -1 on error
        #See back of call rule paper for example.
        call_list_after_weight = list(map(operator.mul, a_player.get_valid_call_list(), self.call_weight_list))
        total = 0
        for index in range(8):
            total += call_list_after_weight[index]
        for index in range(8):
            call_list_after_weight[index] = (call_list_after_weight[index]/total)
            if index != 0:
                call_list_after_weight[index] = call_list_after_weight[index] + call_list_after_weight[index-1]
        call_to_make = random.random(0, 1) #generate a random floating pt. number between 0 and 1
        for index in range(8):
            if call_to_make <= call_list_after_weight[index]:
                return index
            else:
                return -1

    def play_card(self, a_player):
        #Should return the index in the valid play list of the card the agent "chooses" to play.
        #In this case, the index returned is a random number between 0 and the length of the valid play list.
        index = random.randint(0, len(a_player.get_hand().get_valid_play_list()))
        while a_player.get_hand().get_valid_play_list()[index] != 1:
            index = random.randint(0, len(a_player.get_hand().get_valid_play_list()))
        return index

# Short code spike to test if using building a dictionary could be used to filter out invalid indices
if __name__ == "__main__":
    # loop to show that it does give different valid numbers when run multiple times
    for i in range(10):
        a_list = []
        for i in range(8):
            a_list.append(random.randint(0,1))
        a_list.append(1) # just forcing there to always be at least one 1 in the list
        # the above is just building a random list that will look something like the valid card list
        print(a_list)
        # Now to actually filter the list
        valid_indices = list({k: v for k, v in zip(range(len(a_list)), a_list) if v != 0}.keys())
        print(valid_indices)
        # This will create a temp dict where the keys are the indices of the input list and the values are the values in that list
        # but the dict will be built in such a way that only if the value isn't 0 does the pair get added.
        # Then the keys are pulled from the dict and turned into a list, this is now a list of all the valid indices
        # and we can freely pick any value from this list.
        # Still feels like there should be a cleaner way to do this.
        valid_indices = [index for index in range(len(a_list)) if a_list[index] != 0]
        print(valid_indices)
        # There was a cleaner way, didn't need the dict at all.
        # This now builds a list containing only the indices where the value is not 0.
        # This is just a more concise way of saying:
        valid_indices = []
        for index in range(len(a_list)):
            if a_list[index] != 0:
                valid_indices.append(index)

        print(valid_indices)
        print(valid_indices[random.randint(0,len(valid_indices)-1)])
    # The advantage of this method, despite being a bit longer and much more complicated and strange, is that
    # it's deterministic, it will always work on the first pass through the code.
    # Whereas if we re-randomize we can't be sure how many times it might take.