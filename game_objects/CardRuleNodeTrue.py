from game_objects import CardRuleNode

class CardRuleNodeTrue(CardRuleNode.CardRuleNode):
    '''
    This singleton node should always return True, while following the existing node behavior.
    '''
    class __TrueNode:
        def __init__(self):
            def eval():
                return True
            self._description = "This node will return True."
            self._evaluator_function = eval
            self._left = True
            self._right = True
    instance = None
    def __new__(cls): #when a new object of this class is requested it will instead see if the
        #instance already exists and either create it and return, or just return that instance
        if not CardRuleNodeTrue.instance:
            CardRuleNodeTrue.instance = CardRuleNodeTrue.__TrueNode()
        return CardRuleNodeTrue.instance
    def __getattr__(self, var_name):
        if var_name == "_left":
            return getattr(self.instance, "_left")
        if var_name == "_right":
            return getattr(self.instance, "_right")
        