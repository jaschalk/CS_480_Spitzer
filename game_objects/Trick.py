from game_objects.Card import Card
class Trick:
    '''
    The Trick class is used to hold onto the cards players have played
    and inform the round when all players have played.
    '''

    def __init__(self, a_round):
        self._parent_round = a_round
        self.set_intial_values() 

    def set_intial_values(self):
        self._winning_player = None
        self._winning_card = Card(-1,"null")
        self._suit_lead = None
        self._played_cards_list = [Card(-1, "null") for i in range(4)]
        self._points_on_trick = 0
        self.__subscribers = {}

#NOTE publish subscribe code spike
    def subscribe_to(self, a_subscriber, a_message):
        if a_message not in self.__subscribers.keys():
            self.__subscribers[a_message] = []
        self.__subscribers[a_message].append(a_subscriber)
        # So does this mean that all the subscribed messages should take no prams?
        # or do we also store the prams in the subscription as well?

    def notify_subscribers(self): # It might be better to split this up into a method for each message
        for message in self.__subscribers.keys(): # Message is expected to be a string
            for subscriber in self.__subscribers[message]:
                if hasattr(subscriber, message):
                    getattr(subscriber, message)(self) # For now I'm going to assume it's passing in itself
                else:
                    raise Exception(f"Subscriber {subscriber} was sent a message it does not understand: {message}")

    def print_message(self, message):
        if "print_test" in self.__subscribers.keys():
            for subscriber in self.__subscribers["print_test"]:
                if hasattr(subscriber, "print_message"):
                    getattr(subscriber, "print_message")(message) # Setting it up this way we can pass in a known message for each subscription
                else:
                    raise Exception(f"Subscriber {subscriber} was sent a message it does not understand: {message}")

    def notifiy_print_message(self):
        self.print_message("This is a test")
#NOTE publish subscribe code spike

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

    def accept_a_card(self, a_card):
        if self._winning_card == Card(-1,"null"):
            self._suit_lead = a_card.get_card_suit()
        if a_card.visit(self._winning_card) is False:
            self._winning_player = self._parent_round.get_players_list()[a_card.get_owning_player()]
            self._winning_card = a_card
        self._parent_round.notify_players_of_played_card()
        self._played_cards_list[a_card.get_owning_player()] = a_card
        self._points_on_trick += a_card.get_point_value()
        for card in self._played_cards_list:
            if card is Card(-1,"null"):
                return
        self.on_trick_fill()

    def on_trick_fill(self):
        self._parent_round.on_trick_end(self._winning_player, self._points_on_trick, self._played_cards_list)
        self.set_intial_values()
