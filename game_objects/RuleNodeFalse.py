class RuleNodeFalse:
    '''
    This singleton node should always return False, while following the existing node behavior.
    '''
    class __FalseNode:
        def __init__(self):
            self._description = "This node will return False."
        def validate(self, *args):
            return False
    instance = None
    def __new__(cls):
        if not RuleNodeFalse.instance:
            RuleNodeFalse.instance = RuleNodeFalse.__FalseNode()
        return RuleNodeFalse.instance
        
    def validate(self, *args):
        return self.instance.validate(*args)