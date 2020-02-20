#from GameObjects import Card

class CardRuleNode:

    _left = None
    _right = None
    _condition = None

    def __init__(self, left_node, right_node, code_block):
        self._left = left_node
        self._right = right_node
        self._condition = code_block

    def validate(self, a_statement): #this isn't quite what I want
        if self._condition(a_statement): #I'm not sure how to handle this behavior
            return self._left.validate(a_statement)
        else:
            return self._right.validate(a_statement)

if __name__ == "__main__":
    true_node = CardRuleNode(True, True, lambda a: True) #these Nodes might need to be subclasses
    false_node = CardRuleNode(False, False, lambda a: False) #these Nodes might need to be subclasses
    test = CardRuleNode(true_node, false_node, lambda a: a==a)
    print(test.validate(True))