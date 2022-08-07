
# This method should be usable as a generic decorator to provide automatic subscriber
# notification to any method that is wrapped by it.
def decorator(func):
    def wrapper(self, *args, **kwargs):
        # NOTE: Since this wrapper is calling the wrapped function first it's guaranteed that function will
        # be finished before the subscribers are notified.
        func(self, *args, **kwargs)
        func_name = func.__name__ # This is a private property and we should see if there's a way to avoid this
        if func_name in self._subscribers.keys():
            for subscriber in self._subscribers[func_name]:
                if hasattr(subscriber, func_name):
                    getattr(subscriber, func_name)(*args, **kwargs)
                else:
                    raise Exception(f"Subscriber {subscriber} was sent a message it does not understand: {func_name}")
    return wrapper