import random
from enums import *
class CustomAgent:

    # Should be able to gauge the strength of a hand and act accordingly
    # Having more good cards should be multiplicatively better, and bad cards multiplicatively worse
    __trump_strengths = [3.5, 3.25, 3.2, 3, 2.8, 2, 1.5, 1.25, 1.1, 1.25, 0.95, 0.8, 0.65, 0.65, 0.65]
    __fail_strengths = [3, 0.25, 0.1, 0.02, 0.02, 0.02]
    _trump_strength = 100
    _clubs_strength = 100
    _spades_strength = 100
    _hearts_strength = 100
    _total_strength = 0

    def __init__(self):
        self.__reset_default_strengths()

    def __reset_default_strengths(self):
        self._trump_strength = 100
        self._clubs_strength = 100
        self._spades_strength = 100
        self._hearts_strength = 100
        self._total_strength = 0

    def gauge_hand_strength(self, a_hand):
        for card in a_hand.get_cards_in_hand():
            if card.get_card_suit() == "trump":
                self._trump_strength *= self.__trump_strengths[card.get_card_rank()]
            elif card.get_card_suit() == "clubs":
                self._clubs_strength *= self.__fail_strengths[card.get_card_rank() - 9]
            elif card.get_card_suit() == "spades":
                self._spades_strength *= self.__fail_strengths[card.get_card_rank() - 9]
            elif card.get_card_suit() == "hearts":
                self._hearts_strength *= self.__fail_strengths[card.get_card_rank() - 9]     
        self._total_strength = self._trump_strength + self._clubs_strength + self._spades_strength + self._hearts_strength
    
    def find_best_callable_ace_suit(self, a_player):
        fail_strengths =[self._clubs_strength, self._spades_strength, self._hearts_strength]
        callable_strengths = []
        for i in range(3):
            callable_strengths.append(fail_strengths[i] * a_player.get_valid_call_list()[i])
        return 1 + callable_strengths.index(max(callable_strengths))
        

    def make_call(self, a_player):
        call_index = -1
        self.gauge_hand_strength(a_player.get_hand())
        if self._total_strength > 42000:
            call_index = Calls.zolo_s_s
        elif self._total_strength > 28000:
            call_index = Calls.zolo_s
        elif self._total_strength > 9000:
            call_index = Calls.zolo
        elif self._total_strength < 2500 and a_player.get_valid_call_list()[Calls.first_trick] == 1:
            call_index = Calls.first_trick
        elif self._total_strength < 2300 and sum(a_player.get_valid_call_list()[Calls.ace_clubs:Calls.ace_hearts]) > 0: # the second condition means this block is only entered if an ace is callable
            call_index = self.find_best_callable_ace_suit(a_player)
        else:
            call_index = Calls.none

        self.__reset_default_strengths()
        return call_index

    def find_card_index_in_hand(self, a_card_list, a_card_id):
        for i in range(len(a_card_list)):
            if a_card_list[i].get_card_id() == a_card_id:
                return i
        raise Exception("Couldn't find an expected card in the hand. " + str([card.get_card_id() for card in a_card_list]) + " Was looking for: " + str(a_card_id))

    

    def play_card(self, a_player, a_game): 
        # This sub function will determine if any card in a given list of card ids is within a provided filter list, returns -1 if it is not
        def can_play_a_card_in_id_list(an_id_list, index_filter_list):
            for card_id in an_id_list:
                if valid_binary_value & 1<<card_id != 0: # can play this ace
                    card_index = self.find_card_index_in_hand(players_card_list, card_id)
                    if card_index in index_filter_list:
                        return card_index
            return -1

        # This sub function will find the index in the players card list of the first card in the given binary_value
        # NOTE: This presupposes that the card it finds will be valid to play, that condition must be verified outside this function!
        def get_index_of_first_card_in(binary_value, is_reversed=False):
            card_to_play_id = 0
            while binary_value % 2 != 1:
                # this will check if the least signifiant digit in binary_value is not a 1, which means that the players hand doesn't have the card with card_to_play_id
                card_to_play_id += 1
                # so increment the card_to_play_id
                binary_value = binary_value >> 1
                # and shift the reversed_binary_value down to the next digit and continue looking
                if binary_value == 0:
                    # no card could be found so return -1
                    return -1
            if not is_reversed:
                return self.find_card_index_in_hand(players_card_list, card_to_play_id)
            else:
                return self.find_card_index_in_hand(players_card_list, 30 - card_to_play_id)
            # lookup what index that id is at and return that value

        # Should attempt to play cards to maximize it's potential point gain

        #   Calculate the binary rep. of the the collection of cards that are valid to play
        aces_ids = [14, 20, 26] # don't include the ace of diamonds in here
        tens_ids = [10, 15, 21, 27]
        kings_ids = [11, 16, 22, 28]
        current_trick = a_game.get_trick()
        current_winning_card = current_trick.get_winning_card()
        players_card_list = a_player.get_cards_in_hand()
        number_of_cards_on_trick = sum([1 for i in range(4) if current_trick.get_played_cards_list()[i] is not None])
        valid_indices = [index for index in range(len(a_player.get_valid_play_list())) if a_player.get_valid_play_list()[index] != 0]
         #^ this will generate a list containing all the indices that are valid cards to play
        valid_binary_value = sum([1<<players_card_list[index].get_card_id() for index in valid_indices])
         #^ this will generate a number whos binary representation has 1's in the locations of the id numbers of the cards that are valid to play
        winning_card_indecies = [index for index in range(len(players_card_list)) if (not current_winning_card.accept(players_card_list[index]))]
         #^ this will generate a list of all the indecies of cards that can be played to take the trick with, can be empty
        reversed_binary_value = int(format(valid_binary_value, '#034b')[:2:-1], 2)
        #^ reversing the binary value so the weakest card can be picked out

        #If has a fail ace that can take the trick play that ace
        ace_index = can_play_a_card_in_id_list(aces_ids, winning_card_indecies)
        if ace_index != -1:
            return ace_index

        #   If leading or 2nd: if no ace, is trump_strength > 550, if yes play highest trump card I can, if no play weakest card(highest rank/index)
        if number_of_cards_on_trick == 0 or number_of_cards_on_trick == 1:
            if self._trump_strength >= 550:
                valid_trump_value = valid_binary_value & 0b00000000000000000011111111111111
                if valid_trump_value != 0:
                    return get_index_of_first_card_in(valid_trump_value)
                    # can just return here because it'll only be called if there is at least 1 valid trump card to play
            
            # this doesn't need to be checked against a -1 return since it's starting with the all the valid values
            return get_index_of_first_card_in(reversed_binary_value, True)

        #   is the winning player my partner? if yes then smear, that is play points to the trick
        if a_player.get_potential_partners_list()[current_winning_card.get_owning_player()] == 1:
            # check if the current winner is my partner

            smear_lists = [tens_ids, aces_ids, kings_ids]
            # can I smear?
            for card_list in smear_lists:
                card_index = can_play_a_card_in_id_list(card_list, valid_indices)
                if card_index != -1:
                    return card_index

        #   If 3rd: if points on trick > 15 and I can take the trick, play the strongest card I can do so with, else throw off weakest card
        if number_of_cards_on_trick == 2:
            if current_trick.get_points_on_trick() >= 15 and len(winning_card_indecies) > 0:
                return get_index_of_first_card_in(valid_binary_value)

#            reversed_binary_value = int(format(valid_binary_value, '#034b')[:2:-1], 2)
            return get_index_of_first_card_in(reversed_binary_value, True)

        #   If last: does any card I can play take the trick? if yes play the card that can do so with the highest point value, if no throw off worst(highest rank/index) card
        if number_of_cards_on_trick == 3:
            if len(winning_card_indecies) > 0: # I have at least 1 card that can take the trick
                card_list_sorted_by_points = sorted(players_card_list, key=lambda card: card.get_point_value(), reverse=True)
                # this list is now the cards the player has sorted so the highest point cards are first
                for index in range(len(card_list_sorted_by_points)):
                    card_at_index_id = card_list_sorted_by_points[index].get_card_id()
                    card_unsorted_index = can_play_a_card_in_id_list([card_at_index_id], winning_card_indecies)
                    if card_unsorted_index != -1:
                        return card_unsorted_index

            # I cannot take the trick
#            reversed_binary_value = int(format(valid_binary_value, '#034b')[:2:-1], 2)
            return get_index_of_first_card_in(reversed_binary_value, True)

        #fall back on playing a card at random if some case was missed above
        print("Custom agent is playing a random card")
        if len(valid_indices) == 1:
            return 0
        temp = valid_indices[random.randint(0,len(valid_indices)-1)]
        return temp