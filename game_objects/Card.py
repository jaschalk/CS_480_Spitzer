
class Card():

    _card_id = None
    _card_suit = None
    _card_rank = None
    _point_value = 0
    _owning_player_index = -1

    #def __init__(self, a_rank, a_suit):
        #Take another look at this. Might not need this at all.
        #self._card_suit = a_suit
        #self._card_rank = a_rank

    def __new__(cls, a_rank, a_suit):
        if a_suit == "trump":
            from game_objects import TrumpCard
            return TrumpCard.TrumpCard(a_rank, a_suit)
        elif a_suit == "null":
            from game_objects import NullCard
            return NullCard.NullCard(a_rank, a_suit)
        else:
            from game_objects import FailCard
            return FailCard.FailCard(a_rank, a_suit)

    def get_card_id(self): #Getters. Shouldn't ever need to set the id, suit, or rank of a card.
        return self._card_id

    def get_card_suit(self):
        return self._card_suit

    def get_card_rank(self):
        return self._card_rank

    def get_owning_player(self):
        return self._owning_player_index

    def set_owning_player(self, a_player_index):
        self._owning_player_index = a_player_index

    def get_point_value(self):
        return self._point_value

    def set_point_value(self, a_rank):
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

    def accept(self, a_card):
        pass

    def visit(self, an_object):
        #Not 100% on this right now, will talk about at some point.
        #Talk to Sark about this and see what his advice is.
        an_object.accept(self)