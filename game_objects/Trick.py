from game_objects.Card import Card
from functools import wraps
from game_objects import NotificationDecorator

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
        self._subscribers = {}

#NOTE publish subscribe code spike
    def subscribe_to(self, a_subscriber, a_message):
        if a_message not in self._subscribers.keys():
            self._subscribers[a_message] = []
        self._subscribers[a_message].append(a_subscriber)
        # So does this mean that all the subscribed messages should take no prams?
        # or do we also store the prams in the subscription as well?

# I think this can get removed now? Since the _notifier can be used, or modified to be used

    def notify_subscribers(self): # It might be better to split this up into a method for each message
        for message in self._subscribers.keys(): # Message is expected to be a string
            for subscriber in self._subscribers[message]:
                if hasattr(subscriber, message):
                    getattr(subscriber, message)(self) # For now I'm going to assume it's passing in itself
                else:
                    raise Exception(f"Subscriber {subscriber} was sent a message it does not understand: {message}")

    # This _notifier method serves as a holder for the generic decorator located elsewhere
    def _notifier(): # pylint: disable=no-method-argument
        decorator = NotificationDecorator.decorator
        return decorator

    @_notifier() # This needs the empty () because it implicitly takes self as an argument otherwise
    def print_message(self, message):
        print("Notification sent")

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
        if Card(-1,"null") not in self._played_cards_list:
            self.on_trick_end()

    def on_trick_end(self):
        self._parent_round.on_trick_end(self._winning_player, self._points_on_trick, self._played_cards_list)
        self.set_intial_values()
