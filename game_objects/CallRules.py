class CallRules:

    def __init__(self): #setup singleton behavior for the rules
        #calls: NC, AC, AS, AH, FT, Z, ZS, ZSS
        self._call_filter = [(0b10,1<<14), #remember to ~ the hand first
                            (0b100,1<<20), #remember to ~ the hand first
                            (0b1000,1<<26), #remember to ~ the hand first
                            (0b10000,(1<<14) + (1<<20) + (1<<26))]

    def validate_calls(self, a_hand): #should the hand store it's numerical representation, or should it be calculated here?
        valid_call_state = 225 #this is the decimal value representing that any player can make NC, Z, ZS, ZSS calls
        hand_binary_representation = a_hand.get_binary_representation()
        for call, value in self._call_filter:
            if hand_binary_representation == 0: # Guard clause to ensure nonsensical values aren't provided when the player has no cards.
                continue
            elif call == 0b10000:
                if (hand_binary_representation & value) == value:
                    valid_call_state += call
            else:
                if ((~hand_binary_representation) & value) == value:
                    valid_call_state += call
        print(valid_call_state)
        return [int(d) for d in bin(valid_call_state)[2:]][::-1]

if __name__ == "__main__":
    print(~0b100 & 0b11 == 0b11)