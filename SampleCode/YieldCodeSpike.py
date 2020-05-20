# We might be able to use yield in the learning agent to permit the normal flow of the game through
# the play card method, rather than the current interupted style.
def func(a_message):
    count = 1
    print("The first")
    yield
    count += 1
    print("The second")
    yield
    count += 1
    print("The third")
    yield
    count += 1
    for i in range(1,10):
        second_func(a_message, i)
        yield
        count += 1
    print(count)

def second_func(a_message, count):
    for _ in range(count):
        print(a_message)
    print()

if __name__ == "__main__":
    test = func("message")
    print(test.__dir__())
    e = None
    count = 0
    while e is not StopIteration:
        print("Running while loop")
        count += 1
        try:
            next(test)
        except StopIteration:
            print("While loop done")
            e = StopIteration
    print(count)