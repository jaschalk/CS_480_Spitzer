from functools import wraps

class Test:
    
    def log_decorator(): # pylint: disable=no-method-argument
        def actual_decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                for arg in args:
                    print(f"Calling Function: {func.__name__} with args {arg}")
                for kwarg in kwargs:
                    print(f"Calling Function: {func.__name__} with kwarg {kwarg} which has the value of {kwargs[kwarg]}")
                return func(*args, **kwargs)
            return wrapper
        return actual_decorator
    
    @log_decorator()
    def bar(self, a_message, count):
        print(a_message*count)

if __name__ == "__main__":
    test = Test()
    test.bar(a_message="test", count=3)