from game_objects.Game import Game
from agents.RandomAgent import RandomAgent
from agents.CustomAgent import CustomAgent
from agents.LearningAgent import Agent

class HumanAgent:

    def make_call(self, a_player):
        valid_call_list = a_player.get_valid_call_list()
        print(f"Your valid call list is: {valid_call_list}")
        cards_in_hand_list = [card.get_card_id() for card in a_player.get_cards_in_hand()]
        print(f"Your cards in hand are: {cards_in_hand_list}")
        valid_call_indices = [index for index in range(len(valid_call_list)) if valid_call_list[index] == 1]
        call_to_play_index = -1
        while call_to_play_index not in valid_call_indices:
            call_to_play_index = int(input("Which call do you want to make?(enter an index)"))
        return call_to_play_index

    def play_card(self, a_player, a_game):
        valid_play_list = a_player.get_valid_play_list()
        cards_in_hand_list = [card.get_card_id() for card in a_player.get_cards_in_hand()]
        print(f"Your cards in hand are: {cards_in_hand_list}")
        playable_cards_list = [cards_in_hand_list[index] for index in range(len(valid_play_list)) if valid_play_list[index] != 0]
        print(f"Your playable cards are: {playable_cards_list}")
        current_trick = a_game.get_trick()
        cards_on_trick = [str(card) for card in current_trick.get_played_cards_list()]
        print(f"The cards on trick are: {cards_on_trick}")
        card_to_play = -1
        while card_to_play not in playable_cards_list:
            card_to_play = int(input("Which card do you want to play?"))
        for index in range(len(cards_in_hand_list)):
            if card_to_play == cards_in_hand_list[index]:
                return index

if __name__ == "__main__":
    agent_types = [HumanAgent(), Agent(), CustomAgent(), RandomAgent()]
    active_game = Game(0, agent_types)
    active_game.play_game()