from game_objects.RuleNodeTrue import RuleNodeTrue
from game_objects.RuleNodeFalse import RuleNodeFalse
from game_objects.RuleNodeUnknown import RuleNodeUnknown
class RuleNode:
    '''
    The Rule Node class is used to hold onto a boolean evaluator function
    whos return value will direct travel within the tree.
    '''

    def __init__(self, description, a_boolean_return_function):
        self._description = description
        self._left = RuleNodeTrue()
        self._right = RuleNodeFalse()
        self._evaluator_function = a_boolean_return_function

    def validate(self, *args):
        if self._evaluator_function(*args):
            return self._left.validate(*args)
        else:
            return self._right.validate(*args)

    def set_left(self, new_left):
        self._left = new_left

    def set_right(self, new_right):
        self._right = new_right

# code spike to test if/how this is working
if __name__ == "__main__":
    true_node = RuleNodeTrue()
    false_node = RuleNodeFalse()
    print(false_node)
    test_node = RuleNodeFalse() #Singleton behavior works as desired, 2 variables address the same memory location
    print(test_node)

    def sample(*args):
        print("is first less than second?")
        return args[0] < args[1]

    def is_less_than_7(*args):
        print("is less than 7?")
        return args[0] < 7 and args[1] < 7

    def sum_greater_than_3(*args):
        print("sum > 3?")
        return (args[0] + args[1]) > 3

    first_node = RuleNode("This node checks if both inputs are less than 7",
                        is_less_than_7)
    second_node = RuleNode("This node compares two numbers and returns true if the first is less than the second",
                        sample)
    third_node = RuleNode("Checks if the two numbers sum is greater than 3",
                        sum_greater_than_3)
    first_node.set_left(second_node)
    second_node.set_left(third_node)
    print("First test: 1 & 2")
    print(first_node.validate(1,2))
    print("Second test: 3 & 2")
    print(first_node.validate(3,2))
    print("Third test: 9 & 8")
    print(first_node.validate(9,8))
    print("Forth test: 2 & 3")
    print(first_node.validate(2,3)) #IT WORKS!!