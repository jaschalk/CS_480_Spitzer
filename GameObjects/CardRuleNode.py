#from GameObjects import Card
from . import CardRuleNodeTrue
class CardRuleNode:

    _left = None
    _right = None
    _condition = None
    _parent_tree = None

    def __init__(self, parent, left_node, right_node, code_block):
        self._parent_tree = parent
        self._left = left_node
        self._right = right_node
        self._condition = code_block

    def validate(self, *args): #this isn't quite what I want
        if self._condition(*args): #I'm not sure how to handle this behavior
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
    print(test.validate(True))