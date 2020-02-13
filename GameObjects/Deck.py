from GameObjects import Card
from random import shuffle

class Deck:
    '''
    The Deck class is used to hold onto, and distribute, the cards at the start of rounds.
    '''
    card_list = []
    
    def __init__(self):
        self.populate_deck()

    def populate_deck(self):
        '''
        Populating the deck will clear the contents of the cardlist and refill it with the proper collection of cards to play the game with.
        '''
        for i in range(15):
            self.card_list.append(Card.Card(i, "trump"))
        for i in range(9,15):
            self.card_list.append(Card.Card(i, "clubs"))
        for i in range(9,15):
            self.card_list.append(Card.Card(i, "spades"))
        for i in range(9,15):
            self.card_list.append(Card.Card(i, "hearts"))
        shuffle(self.card_list)

    def deal_cards_to(self, targetPlayer):
        '''
        This method will cause 8 cards to visit the targetPlayer. 
        '''
        for i in range(8):
            targetPlayer.accept(self.card_list.pop())
            