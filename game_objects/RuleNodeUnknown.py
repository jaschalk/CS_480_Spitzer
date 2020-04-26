class RuleNodeUnknown:
    '''
    This singleton node should return the string "unknown", while following the existing node behavior.
    '''
    class __UnknownNode:
        def __init__(self):
            self._description = "This node will return the string 'unknown'."
        def validate(self, *args):
            return "unknown"
    instance = None
    def __new__(cls):
        if not RuleNodeUnknown.instance:
            RuleNodeUnknown.instance = RuleNodeUnknown.__UnknownNode()
        return RuleNodeUnknown.instance
        
    def validate(self, *args):
        return self.instance.validate(*args)