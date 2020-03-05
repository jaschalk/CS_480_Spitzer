from agents.agent import Agent

class CustomAgent(Agent):

    # Should be able to gauge the strength of a hand and act accordingly
    # Having more good cards should be multiplicatively better, and bad cards multiplicatively worse
    __trump_strengths = [3.5, 3.25, 3.2, 3, 2.8, 2, 1.5, 1.25, 1.1, 1.25, 0.95, 0.8, 0.65, 0.65, 0.65]
    __fail_strengths = [3, 0.25, 0.1, 0.02, 0.02, 0.02]
    _trump_strength = 100
    _clubs_strength = 100
    _spades_strength = 100
    _hearts_strength = 100
    _total_strength = 0

    def gauge_hand_strength(self, a_hand):
        for card in a_hand.get_cards_in_hand():
            if card.get_suit() == "trump":
                self._trump_strength *= self.__trump_strengths[card.get_card_rank()]
            elif card.get_suit() == "clubs":
                self._clubs_strength *= self.__fail_strengths[card.get_card_rank()]
            elif card.get_suit() == "spades":
                self._spades_strength *= self.__fail_strengths[card.get_card_rank()]
            elif card.get_suit() == "hearts":
                self._hearts_strength *= self.__fail_strengths[card.get_card_rank()]     
        self._total_strength = self._trump_strength + self._clubs_strength + self._spades_strength + self._hearts_strength
    
    def find_best_callable_ace_suit(self, a_player):
        fail_strengths =[self._clubs_strength, self._spades_strength, self._hearts_strength]
        if a_player.get_valid_call_list()[3] == 1 and a_player.get_valid_call_list()[2] == 1 and a_player.get_valid_call_list()[1] == 1:
            return fail_strengths.index(max(fail_strengths))
        elif a_player.get_valid_call_list()[3] == 1 and a_player.get_valid_call_list()[2] == 1:
            return fail_strengths.index(max(fail_strengths[:1]))
        elif a_player.get_valid_call_list()[2] == 1 and a_player.get_valid_call_list()[1] == 1:
            return fail_strengths.index(max(fail_strengths[1:2]))

    def make_call(self, a_player):
        self.gauge_hand_strength(a_player.get_hand()) #cutoffs ZSS 40K, ZS 10K, Z 4K, A >1600, FT >1800, else no call
        if self._total_strength > 40000:
            return 7 # should make these not "magic numbers"
        elif self._total_strength > 10000:
            return 6
        elif self._total_strength > 4000:
            return 5
        elif self._total_strength < 1800 and a_player.get_valid_call_list()[4] == 1:
            return 4
        elif self._total_strength < 1600:
            return self.find_best_callable_ace_suit(a_player)
        else:
            return 0

    def play_card(self, game_state):
        pass
