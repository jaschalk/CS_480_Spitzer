from game_objects.Card import Card

class TrumpCard(Card):
    '''
    The Trump Card class is used to represent cards of the trump suits.
    '''

    def __init__(self, a_rank, a_suit):
        self._card_suit = "trump"
        self._card_rank = a_rank
        self._card_id = a_rank
        self.set_point_value(a_rank)
        self._owning_player_index = -1
    
    def __new__(cls, a_rank, a_suit):
       return object.__new__(cls) 

    def accept(self, a_card):
        if a_card._card_suit == "trump":
            if self.get_card_rank() < a_card.get_card_rank():
                return True
            else:
                return False
        else:
            return True