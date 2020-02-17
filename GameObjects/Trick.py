from GameObjects import Player
from GameObjects import Card
class Trick:

    parent_round = None
    suit_lead = None
    winnning_player = None
    winning_card = None
    leading_player = None
    points_on_trick = 0
    played_cards_list = [None, None, None, None]

    def __init__(self, aRound, aPlayer):
        self.parent_round = aRound
        self.leading_player = aPlayer

    def accept(self, aCard):
       if self.suit_lead is None:
           self.suit_lead = aCard.get_suit()
           self.winning_card = aCard
       else:
           if self.winning_card.accept(aCard) is False:
               self.winning_player = aCard.get_owning_player()
               self.winning_card = aCard
       self.played_cards_list[aCard.get_owning_player()] = aCard #don't append the cards, replace at the player index to preserve play order
       self.points_on_trick += aCard.get_point_value()
       if len(self.played_cards_list) == 4:#the trick is now done, process accordingly
           self.parent_round.on_trick_end(self.winning_player, self.points_on_trick, self.played_cards_list)