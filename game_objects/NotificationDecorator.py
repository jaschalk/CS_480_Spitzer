
# This method should be usable as a generic decorator to provide automatic subscriber
# notification to any method that is wrapped by it.
def decorator(func):
    def wrapper(self, *args, **kwargs):
        # NOTE: Since this wrapper is calling the wrapped function first it's guaranteed that function will
        # be finished before the subscribers are notified.
        func(self, *args, **kwargs)
        func_name = func.__name__
        if func_name in self._subscribers.keys():
            for subscriber, message in self._subscribers[func_name]:
                if hasattr(subscriber, message):
                    getattr(subscriber, message)(*args, **kwargs)
                else:
                    raise Exception(f"Subscriber {subscriber} was sent a message it does not understand: {message}")
    return wrapper