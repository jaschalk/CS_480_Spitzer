from game_objects import Card

class NullCard(Card.Card):

    class __NullCard:
        def __init__(self):
            #Probably change this. unsure how to structure as of yet.
            pass
    #Think about this behavior some more...
    instance = None
    def __new__(cls):
        if not NullCard.instance:
            NullCard.instance = NullCard.__NullCard()
        return NullCard.instance

    def get_card_id(self):
        return None
    
    def get_card_suit(self):
        return None

    def get_card_rank(self):
        return None

    def accept(self, a_card):
        return False