#I'm guessing we want this to inherit from the card class?
#Do I need to import Card or does it know to inherit just based on the syntax?
class FailCard(Card):

    def __init__(self):
        Card.__init__(self, self._card_rank, self._card_suit) #Is this the correct rank and suit?

    def accept_fail(self, a_fail_card):
        if self.get_card_suit == a_fail_card.get_card_suit(): #Can double equals work for string comparison in python?
            if self.get_card_rank() < a_card.get_card_rank():
                return True
            else:
                return False
        else:
            return True