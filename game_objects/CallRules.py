class CallRules:

    def __init__(self): #setup singleton behavior for the rules
        #calls: NC, AC, AS, AH, FT, Z, ZS, ZSS
        self._call_filter = [(2,1<<14), #remember to ~ the hand first
                            (4,1<<20), #remember to ~ the hand first
                            (8,1<<26), #remember to ~ the hand first
                            (16,1<<14 + 1<<20 + 1<<26)]

    def validate_calls(self, a_hand): #should the hand store it's numerical representation, or should it be calculated here?
        valid_call_state = 225 #this is the decimal value representing that any player can make NC, Z, ZS, ZSS calls
        hand_binary_representation = a_hand.binary_representation()
        for call, value in self._call_filter:
            if call == 4:
                if hand_binary_representation & value == value:
                    valid_call_state += call
            else:
                if ~hand_binary_representation & value == value:
                    valid_call_state += call

        return [int(d) for d in bin(valid_call_state)[2:]][::-1]