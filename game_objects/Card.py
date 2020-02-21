from abc import ABC, abstractmethod

class Card(ABC):
    
    _card_id = None
    _card_suit = None
    _card_rank = None
    _point_value = 0

    def __init__(self, a_rank, a_suit): #Constructor. Set suit and rank to be the values passed in, calculate index based on suit offset and rank.
        self._card_suit = a_suit
        self._card_rank = a_rank
        if self._card_suit == "clubs":
            self._card_id = (self._card_rank + 5)
        elif self._card_suit == "spades":
            self._card_id = (self._card_rank + 11)
        elif self._card_suit == "hearts":
            self._card_id = (self._card_rank + 17)
        else:
            self._card_id = self._card_rank
        if self._card_rank == 0 or self._card_rank in range(2, 5):
            self._point_value = 3
        elif self._card_rank in range(5, 9):
            self._point_value = 2
        elif self._card_rank == 9:
            self._point_value = 11
        elif self._card_rank == 10:
            self._point_value = 10
        elif self._card_rank == 11:
            self._point_value = 4
        else:
            self._point_value = 0


    def get_card_id(self): #Getters. Shouldn't ever need to set the id, suit, or rank of a card.
        return self._card_id
    
    def get_card_suit(self):
        return self._card_suit

    def get_card_rank(self):
        return self._card_rank

    @abstractmethod
    def accept(self, a_card):
        '''
        if self.get_card_suit() == "trump":
            if a_card.get_card_suit() == "trump":
                return self.accept_trump(self, a_card)
            else:
                return True
        else:
            if a_card.get_card_suit() == "trump":
                return False
            else:
                return self.accept_fail(self, a_card)
        '''

    def visit(self, an_object):
        #Not 100% on this right now, will talk about at some point.
        #Talk to Sark about this and see what his advice is.
        an_object.accept(self)