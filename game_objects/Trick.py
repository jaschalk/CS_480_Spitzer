from game_objects.Card import Card
class Trick:
    '''
    The Trick class is used to hold onto the cards players have played
    and inform the round when all players have played.
    '''

    def __init__(self, a_round):
        self._parent_round = a_round
        self._winning_card = Card(-1,"null")
        self._suit_lead = None
        self._winning_player = None
        self._played_cards_list = [None, None, None, None]
        self._points_on_trick = 0

    def get_parent_round(self):
        return self._parent_round

    def get_suit_lead(self):
        return self._suit_lead

    def get_winning_player(self):
        return self._winning_player

    def get_winning_card(self):
        return self._winning_card

    def get_points_on_trick(self):
        return self._points_on_trick

    def get_played_cards_list(self):
        return self._played_cards_list

    def accept(self, a_card):

        if self._winning_card == Card(-1,"null"):
            self._suit_lead = a_card.get_card_suit()
        if self._winning_card.accept(a_card) is False:
            self._winning_player = self._parent_round.get_players_list()[a_card.get_owning_player()]
            self._winning_card = a_card
        self._parent_round.notify_players_of_played_card()
        self._played_cards_list[a_card.get_owning_player()] = a_card
        self._points_on_trick += a_card.get_point_value()
        for card in self._played_cards_list:
            if card is None:
                return
        self.on_trick_fill()

    def on_trick_fill(self):
        self._parent_round.on_trick_end(self._winning_player, self._points_on_trick, self._played_cards_list)
        self._played_cards_list = [None, None, None, None]
        self._winning_card = Card(-1, "null")
        self._points_on_trick = 0
