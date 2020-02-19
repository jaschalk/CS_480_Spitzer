from GameObjects import Card

class TrumpCard(Card.Card):

    def __init__(self):
        Card.Card.__init__(self, self._card_rank, "trump") #Is this the correct rank?

    def accept_trump(self, a_trump_card): #A trump card accepts a trump card.
        if self.get_card_rank() < a_trump_card.get_card_rank():
            return True
        else:
            return False