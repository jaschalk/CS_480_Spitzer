from game_objects import Card

class NullCard(Card.Card):
    '''
    The Null Card class is used to represent the absence of a card.
    '''

    class __NullCard:
        def __init__(self, a_rank, a_suit):
            pass
        def accept_a_card(self, a_card):
            return False
        def __str__(self):
            return "None"
    instance = None
    def __new__(cls, a_rank, a_suit):
        if not NullCard.instance:
            NullCard.instance = NullCard.__NullCard(a_rank, a_suit)
        return NullCard.instance