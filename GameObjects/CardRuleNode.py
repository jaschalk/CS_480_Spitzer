#from GameObjects import Card
from . import CardRuleNodeTrue
class CardRuleNode:

    _left = None
    _right = None
    _evaluator_function = None
    _parent_tree = None

    def __init__(self, parent, left_node, right_node, code_block):
        self._parent_tree = parent
        self._left = left_node
        self._right = right_node
        self._evaluator_function = code_block #this should always be a function that returns True/False

    def validate(self, *args): #this might work?
        if self._evaluator_function(*args):
            return self._left.validate(*args)
        else:
            return self._right.validate(*args)

if __name__ == "__main__":
    true_node = CardRuleNodeTrue.CardRuleNodeTrue()
    false_node = CardRuleNodeTrue.CardRuleNodeTrue()
    def sample(a, b):
        if a < b:
            return True
    test = CardRuleNode(None, true_node, false_node, sample)
    print(test.validate((1,2))) #since the sample function takes 2 parameters a tuple containing those parameters
                                #must be passed into the validate method