
class RuleNodeTrue:
    '''
    This singleton node should always return True, while following the existing node behavior.
    '''
    class __TrueNode:
        def __init__(self):
            self._description = "This node will return True."
        def validate(self, *args):
            return True
    instance = None
    def __new__(cls):
        if not RuleNodeTrue.instance:
            RuleNodeTrue.instance = RuleNodeTrue.__TrueNode()
        return RuleNodeTrue.instance
    
    def validate(self, *args):
        return self.instance.validate(*args)