from enums import Calls, CardBinary
class CallRules:

    def __init__(self): #setup singleton behavior for the rules
        #calls: NC, AC, AS, AH, FT, Z, ZS, ZSS
        self._call_filter = [(1<<Calls.ace_clubs.value, CardBinary.ace_clubs.value), #remember to ~ the hand first
                            (1<<Calls.ace_spades.value, CardBinary.ace_spades.value), #remember to ~ the hand first
                            (1<<Calls.ace_hearts.value, CardBinary.ace_hearts.value), #remember to ~ the hand first
                            (1<<Calls.first_trick.value, CardBinary.ace_clubs.value
                                                        + CardBinary.ace_spades.value
                                                        + CardBinary.ace_hearts.value)]

    def validate_calls(self, a_hand):
        valid_call_state = ((1<<Calls.none.value)
                             + (1<<Calls.zolo.value)
                             + (1<<Calls.zolo_s.value)
                             + (1<<Calls.zolo_s_s.value))
        hand_binary_representation = a_hand.get_binary_representation()
        for call, value in self._call_filter:
            if hand_binary_representation == 0: # Guard clause to ensure nonsensical values aren't provided when the player has no cards.
                continue
            elif call == (1<<Calls.first_trick.value):
                if (hand_binary_representation & value) == value:
                    valid_call_state += call
            else:
                if ((~hand_binary_representation) & value) == value:
                    valid_call_state += call
        print(valid_call_state)
        return [int(d) for d in bin(valid_call_state)[2:]][::-1]