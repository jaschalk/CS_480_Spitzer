from game_objects import CardRuleNode
class CardRuleNodeFalse(CardRuleNode.CardRuleNode):
    '''
    This singleton node should always return False, while following the existing node behavior.
    '''
    class __FalseNode:
        def __init__(self):
            def eval():
                return False
            self._description = "This node will return False."
            self._evaluator_function = eval
            self._left = False
            self._right = False
    instance = None
    def __new__(cls): #when a new object of this class is requested it will instead see if the
        #instance already exists and either create it and return, or just return that instance
        if not CardRuleNodeFalse.instance:
            CardRuleNodeFalse.instance = CardRuleNodeFalse.__FalseNode()
        return CardRuleNodeFalse.instance
    def __getattr__(self, var_name):
        if var_name == "_left":
            return getattr(self.instance, "_left")
        if var_name == "_right":
            return getattr(self.instance, "_right")
        