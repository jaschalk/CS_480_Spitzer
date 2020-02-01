from GameObjects import Player
from GameObjects import FailCard
from GameObjects import TrumpCard
class Trick:

    parentGame = None
    suitLead = None
    winnningPlayer = None
    containedCards = []

    def __init__(self):
        pass

    def accept(self, aCard):
        if self.winnningPlayer is not None:
            pass
