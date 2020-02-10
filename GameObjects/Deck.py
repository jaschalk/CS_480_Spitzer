from GameObjects import Card
from random import shuffle

class Deck:
    '''
    The Deck class is used to hold onto, and distribute, the cards at the start of rounds.
    '''
    cardlist = []
    
    def __init__(self):
        self.populate_deck()

    def populate_deck(self):
        '''
        Populating the deck will clear the contents of the cardlist and refill it with the proper collection of cards to play the game with.
        '''
        for i in range(14): #highest rank is expected to be 0 and lowest 13
            if i < 8:
                self.cardlist.append(Card(i, "trump"))
            elif i != 13:
                self.cardlist.append(Card(i, "trump"))
                self.cardlist.append(Card(i, "spades"))
                self.cardlist.append(Card(i, "hearts"))
                self.cardlist.append(Card(i, "clubs"))
            else:
                self.cardlist.append(Card(i, "spades"))
                self.cardlist.append(Card(i, "hearts"))
                self.cardlist.append(Card(i, "clubs"))
        shuffle(self.cardlist)

    def deal_cards_to(self, targetPlayer):
        '''
        This method will cause 8 cards to visit the targetPlayer. 
        '''
        for i in range(8):
            tempCard = self.cardlist.pop()
            targetPlayer.accept(tempCard)
            

