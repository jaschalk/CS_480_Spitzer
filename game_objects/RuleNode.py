from game_objects import RuleNodeTrue
from game_objects import RuleNodeFalse
from game_objects import RuleNodeUnknown
class RuleNode: #this might be generic enough to handle the nodes for both trees?
    _description = "" #is this needed/desired?
    _left = None
    _right = None
    _evaluator_function = None
    _parent_tree = None #this might be redundant

    def __init__(self, parent, description, code_block):
        # it might make more sense to have the left default to true and the right false
        # then make setter methods to assign new left and right nodes
        # that way we wouldn't have to build the tree from the leaves up
        self._description = description
        self._parent_tree = parent
        self._left = RuleNodeTrue.RuleNodeTrue()
        self._right = RuleNodeFalse.RuleNodeFalse()
        self._evaluator_function = code_block #this should always be a function that returns True/False

    def validate(self, *args):
        if self._evaluator_function(*args):
            return self._left.validate(*args)
        else:
            return self._right.validate(*args)

    def set_left(self, new_left):
        self._left = new_left

    def set_right(self, new_right):
        self._right = new_right

if __name__ == "__main__":
    true_node = RuleNodeTrue.RuleNodeTrue()
    false_node = RuleNodeFalse.RuleNodeFalse()
    print(false_node)
    test_node = RuleNodeFalse.RuleNodeFalse() #Singleton behavior works as desired, 2 variables address the same memory location
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

    first_node = RuleNode(None, "This node checks if both inputs are less than 7",
                        is_less_than_7)
    second_node = RuleNode(None, "This node compares two numbers and returns true if the first is less than the second",
                        sample)
    third_node = RuleNode(None, "Checks if the two numbers sum is greater than 3",
                        sum_greater_than_3)
    first_node.set_left(second_node)
    second_node.set_left(third_node)
    print("First test: 1 & 2")
    print(first_node.validate(1,2)) #since the "sample" function takes 2 parameters, then bundles those into a tuple which
                                #must be passed into the validate method
    print("Second test: 3 & 2")
    print(first_node.validate(3,2))
    print("Third test: 9 & 8")
    print(first_node.validate(9,8))
    print("Forth test: 2 & 3")
    print(first_node.validate(2,3)) #IT WORKS!!