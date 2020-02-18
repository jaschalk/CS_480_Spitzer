class Card:
    
    _card_id = None
    _card_suit = None
    _card_rank = None

    def __init__(self, a_rank, a_suit): #Constructor. Set suit and rank to be the values passed in, calculate index based on suit offset and rank.
        self._card_suit = a_suit
        self._card_rank = a_rank
        if self._card_suit == "clubs":
           self._card_id = (self._card_rank + 5)
        elif self._card_suit == "spades":
            self._card_id = (self._card_rank + 11)
        elif self._card_suit == "hearts":
            self._card_id = (self._card_rank + 17)
        else:
            self._card_id = self._card_rank

    def get_card_id(self): #Getters. Shouldn't ever need to set the id, suit, or rank of a card.
        return self._card_id
    
    def get_card_suit(self):
        return self._card_suit

    def get_card_rank(self):
        return self._card_rank

    def accept(self, a_card): #This is a lot of conditionals. Is there a better way to do this?
        if a_card.get_card_suit() == "trump":
            if self.get_card_suit() == "trump":
                if self.get_card_rank() < a_card.get_card_rank:
                    return True
                else:
                    return False
            else:
                return False
        else:
            if self.get_card_suit() == "trump":
                return True
            else:
                if self.get_card_suit == a_card.get_card_suit():
                    if self.get_card_rank() < a_card.get_card_rank:
                        return True
                    else:
                        return False
                else:
                    return True

    def visit(self, a_card_rule_object):
        #What should belong in this method?
        #Check out principles
        pass