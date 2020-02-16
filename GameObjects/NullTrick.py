from GameObjects import Trick
from GameObjects import Player
from GameObjects import Round

class NullTrick(Trick.Trick): #what is this actually going to be used for?
    
    def accept(self, a_card): #in theory I want to use this to eliminate the need to do first card on trick checks
        new_trick = Trick.Trick(self._parent_round, self._leading_player, a_card.get_suit())
        self._parent_round.set_current_trick(new_trick)
        new_trick.accept(a_card)