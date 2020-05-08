from functools import wraps

class Test:
    
    def log_decorator():
        def actual_decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                if True:
                    for arg in args:
                        print(f"Calling Function: {func.__name__} with args {arg}")
                return func(*args, **kwargs)
            return wrapper
        return actual_decorator
    
    @log_decorator()
    def bar(self, a_message):
        print(a_message)

test = Test()

test.bar("something")