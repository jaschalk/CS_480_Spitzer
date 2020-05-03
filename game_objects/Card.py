
class Card():
    '''
    The Card class is used as a generator for its subclasses.
    '''

    def __init__(self, a_rank, a_suit):
        self._card_id = -1
        self._card_suit = None
        self._card_rank = -1

    def __new__(cls, a_rank, a_suit):
        if a_suit == "trump":
            from game_objects import TrumpCard #If these are up at the top, they cause circulat import depednencies
            return TrumpCard.TrumpCard(a_rank, a_suit)
        elif a_suit == "null":
            from game_objects import NullCard
            return NullCard.NullCard(a_rank, a_suit)
        else:
            from game_objects import FailCard
            return FailCard.FailCard(a_rank, a_suit)

    def __str__(self):
        return str(self._card_id)

    def get_card_id(self):
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

    def accept_a_card(self, a_card):
        pass

    def visit(self, an_object):
        return an_object.accept_a_card(self)