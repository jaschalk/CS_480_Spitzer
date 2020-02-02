from GameObjects import Player
from GameObjects import FailCard
from GameObjects import TrumpCard
class Trick:

    parentRound = None
    suitLead = None
    winnningPlayer = None
    leadingPlayer = None
    playedCards = []

    def __init__(self, aRound, aPlayer):
        self.parentRound = aRound
        self.leadingPlayer = aPlayer

    def accept(self, aCard):
        if self.winnningPlayer is not None:
            isValid = self.winnningPlayer.accept(aCard)
            if isValid:
                self.playedCards.append(aCard)
        else:
            self.winnningPlayer = aCard.playingPlayer
