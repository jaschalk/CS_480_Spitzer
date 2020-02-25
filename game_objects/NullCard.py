from game_objects import Card

class NullCard(Card.Card):

    class __NullCard:
        def __init__(self):
            pass
        def accept(self, a_card):
            return False
    instance = None
    def __new__(cls):
        if not NullCard.instance:
            NullCard.instance = NullCard.__NullCard()
        return NullCard.instance