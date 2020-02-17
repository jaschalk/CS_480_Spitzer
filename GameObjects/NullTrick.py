from GameObjects import Trick
from GameObjects import Player
from GameObjects import Round

class NullTrick(Trick.Trick): #what is this actually going to be used for?

    class __NullTrick(Trick.Trick):
        pass
    
    instance = None # this might set up a singleton behavior
    def __init__(self, a_round, a_player, a_suit = None):
        if not NullTrick.instance:
            NullTrick.instance = NullTrick.__NullTrick(a_round, a_player, a_suit)
        else:
            NullTrick.instance.a_round = a_round
            NullTrick.instance.a_player = a_player
            NullTrick.instance.a_suit = a_suit

    def accept(self, a_card): #in theory I want to use this to eliminate the need to do first card on trick checks
        new_trick = Trick.Trick(self._parent_round, self._leading_player, a_card.get_suit())
        self._parent_round.set_current_trick(new_trick)
        new_trick.accept(a_card)