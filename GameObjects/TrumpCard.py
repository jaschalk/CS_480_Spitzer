from GameObjects import Card

class TrumpCard(Card.Card):

    def __init__(self):
        #Probably change this. unsure how to structure as of yet.
        Card.Card.__init__(self, self._card_rank, "trump")

    def accept(self, a_card): #A trump card accepts a card.
        if a_card._card_suit == "trump":
            if self.get_card_rank() < a_card.get_card_rank():
                return True
            else:
                return False
        else:
            return True