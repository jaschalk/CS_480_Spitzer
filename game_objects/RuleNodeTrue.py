
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
    def __new__(cls): #when a new object of this class is requested it will instead see if the
        #instance already exists and either create it and return, or just return that instance
        if not RuleNodeTrue.instance:
            RuleNodeTrue.instance = RuleNodeTrue.__TrueNode()
        return RuleNodeTrue.instance
    
    def validate(self, *args):
        self.instance.validate(*args)