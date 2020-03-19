from game_objects import Card
from random import shuffle

class Deck:
    '''
    The Deck class is used to hold onto, and distribute, the cards at the start of rounds.
    '''
    _card_list = []
    
    def __init__(self):
        self.populate_deck()

    def populate_deck(self):
        '''
        Populating the deck will clear the contents of the cardlist and refill it with the proper collection of cards to play the game with.
        '''
        self._card_list.clear()
        for i in range(15):
            if i < 14:
                self._card_list.append(Card.Card(i, "trump"))
            if i > 8:
                self._card_list.append(Card.Card(i, "clubs"))
                self._card_list.append(Card.Card(i, "spades"))
                self._card_list.append(Card.Card(i, "hearts"))

        shuffle(self._card_list)

    def deal_cards_to(self, targetPlayer):
        '''
        This method will cause 8 cards to visit the targetPlayer. 
        '''
        for i in range(8):
            self._card_list.pop().visit(targetPlayer)

    def get_card_list(self):
        return self._card_list
            