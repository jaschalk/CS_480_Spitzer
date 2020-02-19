#I'm guessing we want this to inherit from the card class?
#Do I need to import Card or does it know to inherit just based on the syntax?
class TrumpCard(Card):

    def __init__(self):
        Card.__init__(self, self._card_rank, "trump") #Is this the correct rank?

    def accept_trump(self, a_trump_card): #A trump card accepts a trump card.
        if self.get_card_rank() < a_trump_card.get_card_rank():
            return True
        else:
            return False