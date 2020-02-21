from GameObjects import CardRuleNode

class CardRuleTree:

    _root = None

    def __init__(self): #this might need to be responsible for building the entire tree of conditions?
        self._root = CardRuleNode.CardRuleNode(self, None, None, None)
        
    def validate_card(self, a_card, a_player, a_round):
        if self._root is not None:
            self._root.validate(a_card, a_player, a_round)
        else:
            raise RuntimeError("Rule tree not built!")