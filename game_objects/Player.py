from game_objects.Hand import Hand
from agents.LearningAgent import Agent

class Player:
    '''
    The Player class is used to provide an interface for an agent to interact with the game
    and hold onto information about their personal game state.
    '''

    def __init__(self, a_game, player_id, an_agent):
        self._player_id = player_id
        self._parent_game = a_game
        self._controlling_agent = an_agent
        self._total_score = 0
        self._score_change_list = []
        self.set_initial_values()

    def set_initial_values(self):
        #When a new round starts this method is called and is used
        #to reset the player's game state to its initial status.
        self._potential_partners_list = [0, 0, 0, 0]
        self._potential_partners_list[self._player_id] = 1
        for index in range(4):
            if index != self._player_id:
                self._potential_partners_list[index] = (1/3)
        self._hand = Hand(self)
        self._valid_call_list = [1, 0, 0, 0, 0, 1, 1, 1]
        self._round_points = 0
        self._trick_points = 0
        self._is_leading = False
        self._cards_played = 0
        self._played_cards_list = [0 for _ in range(32)]

    def get_starting_cards(self):
        return self._hand.get_starting_cards()

    def get_player_id(self):
        return self._player_id

    def get_trick_points(self):
        return self._trick_points

    def set_trick_points(self, a_trick_points):
        self._trick_points = a_trick_points

    def get_total_score(self):
        return self._total_score

    def get_score_change_list(self):
        return self._score_change_list

    def set_total_score(self, a_total_score):
        self._total_score = a_total_score

    def expand_score_change_list(self):
        self._score_change_list.append(0)

    def update_total_score(self, a_score):
        self._score_change_list[-1] = a_score
        self._total_score += a_score
        
    def get_round_points(self):
        return self._round_points

    def set_round_points(self, a_round_points):
        self._round_points = a_round_points

    def get_valid_call_list(self):
        return self._valid_call_list

    def set_valid_call_list(self, a_valid_call_list):
        self._valid_call_list = a_valid_call_list

    def get_potential_partners_list(self):
        return self._potential_partners_list

    def set_potential_partners_list(self, a_potential_partners_list):
        self._potential_partners_list = a_potential_partners_list

    def get_hand(self):
        return self._hand

    def get_cards_in_hand(self):
        return self.get_hand().get_cards_in_hand()

    def get_hand_binary_representation(self):
        return self._hand.get_binary_representation()

    def set_hand(self, a_hand):
        self._hand = a_hand

    def get_cards_played(self):
        return self._cards_played

    def get_cards_played_as_list(self):
        return self._played_cards_list

    def get_is_leading(self):
        return self._is_leading

    def get_valid_play_list(self):
        return self.get_hand().get_valid_play_list()

    def initialze_valid_play_list(self):
        self._hand.initialze_valid_play_list()

    def get_controlling_agent(self):
        return self._controlling_agent

    def set_controlling_agent(self, an_agent):
        self._controlling_agent = an_agent

    def accept_a_card(self, a_card):
        a_card.set_owning_player(self.get_player_id())
        a_card.visit(self._hand)

    def play_card_to(self, a_trick):
        #Player asks agent to pick a card to play. The value returned from the agent is used to ask the hand to play a card at the index returned to the trick.
        card_to_play_index = self._controlling_agent.play_card(self, self._parent_game)
        card_id = self._hand.get_card_at_index(card_to_play_index).get_card_id()
        self._played_cards_list[card_id] = 1
        self._cards_played += 1<<(card_id)
        self._hand.play_card_at_index(a_trick, card_to_play_index)

    def learn(self):
        if isinstance(self._controlling_agent, Agent):
            self._controlling_agent.learn(self, self._parent_game)

    def log_played_card(self, card_id):
        self._cards_played += 1<<card_id

    def play_card_at_index(self, a_trick, card_to_play_index):
        self._hand.play_card_at_index(a_trick, card_to_play_index)

    def validate_card(self, a_card):
        return self._parent_game.validate_card(a_card, self)

    def determine_valid_play_list(self):
        self._hand.determine_valid_play_list()

    def determine_potential_partners(self):
        _results = [None, None, None, None]
        _unknowns = 0
        # The goal here is to store all the return strings so we know the full partner state before we update anything
        for index in range(4):
            if index != self._player_id:
                _result = self._parent_game.validate_partners(self, index)
                if _result == "unknown":
                    _unknowns += 1
                _results[index] = _result
            else:
                _results[index] = "target is my partner"

        for index in range(4):
            if _results[index] == "target is my partner":
                self._potential_partners_list[index] = 1
            elif _results[index] == "target is not my partner":
                self._potential_partners_list[index] = 0
            else:
                self._potential_partners_list[index] = 1/_unknowns

    def ask_for_call(self):
        #Player asks agent to make a call. The value returned from the agent is then used to update the round based on the index of the call made.
        self.determine_valid_calls()
        index_of_call_made = self._controlling_agent.make_call(self)
        self._parent_game.update_call(self._player_id, index_of_call_made)

    def determine_valid_calls(self):
        self._valid_call_list = self._parent_game.validate_calls(self._hand)

    def does_play_continue(self):
        if len(self._hand.get_cards_in_hand()) == 0:
            return False
        else:
            return True