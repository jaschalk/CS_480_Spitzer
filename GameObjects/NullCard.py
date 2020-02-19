class NullCard:

    _card_id = None
    _card_suit = None
    _card_rank = None

    def __init__(self, a_rank, a_suit):
        pass

    def get_card_id(self):
        return None
    
    def get_card_suit(self):
        return None

    def get_card_rank(self):
        return None

    def accept(self, a_card):
        return False