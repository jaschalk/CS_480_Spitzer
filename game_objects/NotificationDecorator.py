
# This method should be usable as a generic decorator to provide automatic subscriber
# notification to any method that is wrapped by it.
def decorator(func):
    def wrapper(self, *args, **kwargs):
        func(self, *args, **kwargs) 
        func_name = func.__name__
        if func_name in self._subscribers.keys():
            for subscriber in self._subscribers[func_name]:
                if hasattr(subscriber, func_name):
                    getattr(subscriber, func_name)(*args, **kwargs)
                else:
                    raise Exception(f"Subscriber {subscriber} was sent a message it does not understand: {func_name}")
    return wrapper