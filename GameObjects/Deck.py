from GameObjects import TrumpCard
from GameObjects import FailCard
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
        for i in range(14):
            if i < 9:
                self.cardlist.append(TrumpCard(i))
            elif i != 14:
                self.cardlist.append(TrumpCard(i))
                self.cardlist.append(FailCard(i, "spades"))
                self.cardlist.append(FailCard(i, "hearts"))
                self.cardlist.append(FailCard(i, "clubs"))
            else:
                self.cardlist.append(FailCard(i, "spades"))
                self.cardlist.append(FailCard(i, "hearts"))
                self.cardlist.append(FailCard(i, "clubs"))
        shuffle(self.cardlist)

    def deal_cards_to(self, targetPlayer):
        '''
        This method will cause 8 cards to visit the targetPlayer. 
        '''
        for i in range(8):
            tempCard = self.cardlist.pop()
            targetPlayer.accept(tempCard)
            

