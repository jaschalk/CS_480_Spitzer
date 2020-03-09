from game_objects.RuleNode import RuleNode
from game_objects.RuleNodeTrue import RuleNodeTrue
from game_objects.RuleNodeFalse import RuleNodeFalse

class CardRuleTree:

    _root = None

    def get_root(self):
        return self._root

    def __init__(self): #this might need to be responsible for building the entire tree of conditions?
                        #is there a way to avoid doing so?

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
            # the ace will be card # 14 + 6*(call_index - 1)
            return 14 + 6*(which_call - 1)

        def get_suit_binary_representation(suit):
#            if suit is None: # why did we need this, I remember we added it for a reason
#                return 0b0
            if suit == "trump":
                return 0b00000000000000000011111111111111
            elif suit == "clubs":
                return 0b00000000000011111100000000000000
            elif suit == "spades":
                return 0b00000011111100000000000000000000
            elif suit == "hearts":
                return 0b11111100000000000000000000000000
            else:
                # raise an error if the suit requested isn't in the valid set, to prevent silent errors
                raise RuntimeError("Get suit binary representation received a request for an invalid suit. " + suit)

        def is_player_leading(*args):
            return args[2].get_leading_player() == args[1]

        def has_one_card(*args):
            return len(args[1].get_hand().get_cards_in_hand()) == 1

        def was_ace_called(*args):
            call_state = args[2].get_call_matrix()
            ace_called = False
            for i in range(4): #query each players index in the call matrix to see if they called an ace
                if(call_state[i][1] == 1 or call_state[i][2] == 1 or call_state[i][3] == 1):
                    ace_called = True

            return ace_called

        def has_called_ace(*args):
            ace_id = get_ace_called_id(*args)
            return (args[1].get_hand().get_binary_representation() & 1<<ace_id) == 1<<ace_id
            # might want to add a method to the player to avoid this Law of Demeter violation

        def has_suit_lead(*args):
            suit_lead = args[2].get_suit_lead()
            suit_lead_binary_representation = get_suit_binary_representation(suit_lead)
            return (args[1].get_hand().get_binary_representation() & suit_lead_binary_representation) != 0
            # might want to add a method to the player to avoid this Law of Demeter violation

        def is_card_called_ace(*args):
            ace_id = get_ace_called_id(*args)
            return args[0].get_card_id() == ace_id

        def does_card_follow_suit(*args):
            suit_lead = args[2].get_suit_lead()
            suit_lead_binary_representation = get_suit_binary_representation(suit_lead)
            return suit_lead_binary_representation & 1<<args[0].get_card_id() != 0

        def does_player_have_trump(*args):
            trump_binary_representation = get_suit_binary_representation("trump")
            return (trump_binary_representation & args[1].get_hand().get_binary_representation() != 0)

        def was_called_ace_suit_lead(*args):
            called_ace_id = get_ace_called_id(*args)
            suit_lead = args[2].get_suit_lead()
            suit_lead_binary_representation = get_suit_binary_representation(suit_lead)
            return (suit_lead_binary_representation & called_ace_id) == 0

        def is_card_trump(*args): #all *args should be: a_card, a_player, a_round in that order
            trump_binary_representation = get_suit_binary_representation("trump")
            return (trump_binary_representation & 1<<args[0].get_card_id()) != 0

        self._root = RuleNode(self, "Returns true if the asking player is leading.", is_player_leading)
        __root_R = RuleNode(self, "Returns true if the player has only one card", has_one_card)
        __root_RR = RuleNode(self, "Returns true if any ace was called.", was_ace_called)
        __root_RRL = RuleNode(self, "Returns true if the asking player has the called ace.", has_called_ace)
        __root_RRLL = RuleNode(self, "Returns true if the card in questions is the called ace.", is_card_called_ace)
        __root_RRLLR = RuleNode(self, "Returns true if the suit of the called ace was lead.", was_called_ace_suit_lead)
        __root_RRLLL = RuleNode(self, "Returns true if the suit of the called ace was lead.", was_called_ace_suit_lead)
        __root_RRR = RuleNode(self, "Returns true if the asking player has cards of the suit lead", has_suit_lead)
        __root_RRRL = RuleNode(self, "Returns true if the card in question is of the suit lead", does_card_follow_suit)
        __root_RRRR = RuleNode(self, "Returns true if the asking player has trump cards.", does_player_have_trump)
        __root_RRRRL = RuleNode(self, "Returns true if the card in question is trump.", is_card_trump)
        self._root.set_right(__root_R)
        __root_R.set_right(__root_RR)
        __root_RR.set_right(__root_RRR)
        __root_RR.set_left(__root_RRL)
        __root_RRR.set_right(__root_RRRR)
        __root_RRR.set_left(__root_RRRL)
        __root_RRL.set_right(__root_RRR)
        __root_RRL.set_left(__root_RRLL)
        __root_RRLL.set_right(__root_RRLLR)
        __root_RRLLR.set_left(RuleNodeFalse())
        __root_RRLLR.set_right(__root_RRR)
        __root_RRLL.set_left(__root_RRLLL)
        __root_RRRR.set_left(__root_RRRRL)
        __root_RRRR.set_right(RuleNodeTrue())
        #this is pretty confusing right now, maybe we can think of a way to clean it up.
        
    def validate_card(self, a_card, a_player, a_round):
        return self._root.validate(a_card, a_player, a_round)