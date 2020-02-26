from game_objects.Card import Card

class FailCard(Card):

    def __init__(self, a_rank, a_suit):
        self._card_suit = a_suit
        self._card_rank = a_rank
        if self._card_suit == "clubs":
            self._card_id = (self._card_rank + 5)
        elif self._card_suit == "spades":
            self._card_id = (self._card_rank + 11)
        elif self._card_suit == "hearts":
            self._card_id = (self._card_rank + 17)
        self.set_point_value(a_rank)

    def __new__(cls, a_rank, a_suit):
        #know we need to do this, unsure of what goes here. 
        return object.__new__(cls)

    def accept(self, a_card):
        if a_card._card_suit == "fail":
            if self.get_card_suit == a_card.get_card_suit():
                if self.get_card_rank() < a_card.get_card_rank():
                    return True
                else:
                    return False
            else:
                return True
        else:
            return False