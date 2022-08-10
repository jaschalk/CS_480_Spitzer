from functools import wraps

def log_decorator():
    def actual_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)
            for subscriber, message in args[0].subscribers[func.__name__]:
                getattr(subscriber, message)(*args[1:], **kwargs)
            return
        return wrapper
    return actual_decorator

class TestHand:

    card_count = 7
    subscribers = {}

    def log_subscriber_message_to_function(self, a_subscriber, message, a_function_name):
        if a_function_name in self.subscribers.keys():
            if a_subscriber not in self.subscribers[a_function_name]:
                self.subscribers[a_function_name].append([a_subscriber, message])
        else:
            self.subscribers[a_function_name] = [[a_subscriber, message]]

    @log_decorator()
    def play_card(self):
        self.card_count -= 1
        print(hand.card_count)

class TestTrick:

    card_count = 0

    def log_played_card(self):
        self.card_count += 1
        print(self.card_count)

    def subscribe_to_with_message(self, a_publisher, a_function_name, message):
        a_publisher.log_subscriber_message_to_function(self, message, a_function_name)

if __name__ == "__main__":
    hand = TestHand()
    trick = TestTrick()
    trick2 = TestTrick()
    trick.subscribe_to_with_message(hand, "play_card", "log_played_card")
    trick2.subscribe_to_with_message(hand, "play_card", "log_played_card")
    hand.play_card()