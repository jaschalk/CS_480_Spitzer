from GameObjects import Player
from GameObjects import Card
class Trick:

    _parent_round = None
    _suit_lead = None
    _winning_player = None
    _winning_card = None
    _leading_player = None
    _points_on_trick = 0
    _played_cards_list = [None, None, None, None]

    def get_suit_lead(self): # suit lead should only be set by the trick accepting a card
        return self._suit_lead

    def get_winning_player(self): # the winning player should only be set by the ending of a trick
        return self._winning_player

    def get_winning_card(self): # the winning card should only be set by the trick accepting cards
        return self._winning_card

    def get_leading_player(self): # the leading player shouldn't be set at anytime other than the creation of a trick
        return self._leading_player

    def get_points_on_trick(self): # the points on trick should only be set by the trick accepting cards
        return self._points_on_trick

    def get_played_cards_list(self): # the only way to set the cards played list should be to play cards to the trick, i.e. the trick accepting cards
        return self._played_cards_list

    def __init__(self, a_round, a_player, a_suit = None): # I don't like that this is taking a suit right now, it seems unintuitive
        self.__parent_round = a_round
        self._leading_player = a_player
        self._suit_lead = a_suit

    def accept(self, a_card):
       if self._suit_lead is None:
           self._suit_lead = a_card.get_suit()
           self._winning_card = a_card
       else:
           if self._winning_card.accept(a_card) is False:
               self._winning_player = a_card.get_owning_player()
               self._winning_card = a_card
       self._played_cards_list[a_card.get_owning_player()] = a_card #don't append the cards, replace at the player index to preserve the owner of the card
       self._points_on_trick += a_card.get_point_value()
       if len(self._played_cards_list) == 4: #the trick is now done, process accordingly
           self.__parent_round.on_trick_end(self._winning_player, self._points_on_trick, self._played_cards_list)