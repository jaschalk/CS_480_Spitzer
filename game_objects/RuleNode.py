from game_objects import RuleNodeTrue
from game_objects import RuleNodeFalse
class RuleNode: #this might be generic enough to handle the nodes for both trees?
    _description = "" #is this needed/desired?
    _left = None
    _right = None
    _evaluator_function = None
    _parent_tree = None

    def __init__(self, parent, description, left_node, right_node, code_block):
        self._description = description
        self._parent_tree = parent
        self._left = left_node
        self._right = right_node
        self._evaluator_function = code_block #this should always be a function that returns True/False

    def validate(self, *args): #this might work?
        if self._evaluator_function(*args): # need a way to unpack the information to be passed in
            return self._left.validate(*args)
        else:
            return self._right.validate(*args)

if __name__ == "__main__":
    true_node = RuleNodeTrue.RuleNodeTrue()
    false_node = RuleNodeFalse.RuleNodeFalse()
    print(false_node)
    test_node = RuleNodeFalse.RuleNodeFalse()
    print(test_node)
    def sample(*args):
        print("is first less than second?")
        if args[0] < args[1]:
            return True
        else:
            return False
    def is_less_than_7(*args):
        print("is less than 7?")
        if args[0] < 7 and args[1] < 7:
            return True
        else:
            return False
    test = RuleNode(None, "This node compares two numbers and returns true if the first is less than the second",
                         true_node, false_node, sample)
    first_node = RuleNode(None, "This node checks if both inputs are less than 7",
                        test, false_node, is_less_than_7)
    print(test.validate(1,2)) #since the "sample" function takes 2 parameters, then bundles those into a tuple which
                                #must be passed into the validate method
    print(first_node.validate(3,2))
    print(first_node.validate(9,8))
    print(first_node.validate(2,3)) #IT WORKS!!