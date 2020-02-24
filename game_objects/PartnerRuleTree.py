from game_objects import RuleNode

class PartnerRuleTree:

    _root = None

    def get_root(self):
        return self._root

    def __init__(self):
        self.root = PartnerRuleNode