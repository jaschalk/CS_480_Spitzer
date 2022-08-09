from functools import wraps

def log_decorator():
    def actual_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)
            for subscriber in args[0].subscribers[func.__name__]:
                getattr(subscriber, func.__name__)()
            return 
        return wrapper
    return actual_decorator

class TestHand:

    card_count = 7
    subscribers = {}

    def log_subscriber(self, a_subscriber, a_function_name):
        if a_function_name in self.subscribers.keys():
            if a_subscriber not in self.subscribers[a_function_name]:
                self.subscribers[a_function_name].append(a_subscriber)
        else:
            self.subscribers[a_function_name] = [a_subscriber]

    @log_decorator()
    def play_card(self):
        self.card_count -= 1
        print(hand.card_count)

class TestTrick:

    card_count = 0

    def play_card(self):
        self.card_count += 1
        print(self.card_count)

    def subscribe_to(self, a_publisher, a_function_name):
        a_publisher.log_subscriber(self, a_function_name)

if __name__ == "__main__":
    hand = TestHand()
    trick = TestTrick()
    trick2 = TestTrick()
    trick.subscribe_to(hand, "play_card")
    trick2.subscribe_to(hand, "play_card")
    hand.play_card()
    