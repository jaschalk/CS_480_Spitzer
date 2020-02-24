from game_objects import Card

class NullCard(Card.Card):

    def __init__(self, a_rank, a_suit):
        #Probably change this. unsure how to structure as of yet.
        pass

    def get_card_id(self):
        return None
    
    def get_card_suit(self):
        return None

    def get_card_rank(self):
        return None

    def accept(self, a_card):
        return False