from game_objects import Card

class FailCard(Card.Card):

    def __init__(self):
        #Probably change this. unsure how to structure as of yet.
        Card.Card.__init__(self, self._card_rank, self._card_suit)

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