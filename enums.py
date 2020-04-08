from enum import Enum

# I'm not sold on using this type of enum, it feels really bulky to address
# i.e. Calls.none.value just feels like to many layers
class Calls(Enum):
    """
    These enums 
    """
    none = 0
    ace_clubs = 1
    ace_spades = 2
    ace_hearts = 3
    first_trick = 4
    zolo = 5
    zolo_s = 6
    zolo_s_s = 7

class CardIds(Enum):
    """
    These enums represent the id number associated with each card
    """
    queen_clubs = 0
    seven_diamonds = 1
    queen_spades = 2
    queen_hearts = 3
    queen_diamonds = 4
    jack_clubs = 5
    jack_spades = 6
    jack_hearts = 7
    jack_diamonds = 8
    ace_diamonds = 9
    ten_diamonds = 10
    king_diamonds = 11
    nine_diamonds = 12
    eight_diamonds = 13
    ace_clubs = 14
    ten_clubs = 15
    king_clubs = 16
    nine_clubs = 17
    eight_clubs = 18
    seven_clubs = 19
    ace_spades = 20
    ten_spades = 21
    king_spades = 22
    nine_spades = 23
    eight_spades = 24
    seven_spades = 25
    ace_hearts = 26
    ten_hearts = 27
    king_hearts = 28
    nine_hearts = 29
    eight_hearts = 30
    seven_hearts = 31

class CardBinary(Enum):
    """
    These enums represent the binary number associated with each card
    """
    queen_clubs = 1<<CardIds.queen_clubs.value
    seven_diamonds = 1<<CardIds.seven_diamonds.value
    queen_spades = 1<<CardIds.queen_spades.value
    queen_hearts = 1<<CardIds.queen_hearts.value
    queen_diamonds = 1<<CardIds.queen_diamonds.value
    jack_clubs = 1<<CardIds.jack_clubs.value
    jack_spades = 1<<CardIds.jack_spades.value
    jack_hearts = 1<<CardIds.jack_hearts.value
    jack_diamonds = 1<<CardIds.jack_diamonds.value
    ace_diamonds = 1<<CardIds.ace_diamonds.value
    ten_diamonds = 1<<CardIds.ten_diamonds.value
    king_diamonds = 1<<CardIds.king_diamonds.value
    nine_diamonds = 1<<CardIds.nine_diamonds.value
    eight_diamonds = 1<<CardIds.eight_diamonds.value
    ace_clubs = 1<<CardIds.ace_clubs.value
    ten_clubs = 1<<CardIds.ten_clubs.value
    king_clubs = 1<<CardIds.king_clubs.value
    nine_clubs = 1<<CardIds.nine_clubs.value
    eight_clubs = 1<<CardIds.eight_clubs.value
    seven_clubs = 1<<CardIds.seven_clubs.value
    ace_spades = 1<<CardIds.ace_spades.value
    ten_spades = 1<<CardIds.ten_spades.value
    king_spades = 1<<CardIds.king_spades.value
    nine_spades = 1<<CardIds.nine_spades.value
    eight_spades = 1<<CardIds.eight_spades.value
    seven_spades = 1<<CardIds.seven_spades.value
    ace_hearts = 1<<CardIds.ace_hearts.value
    ten_hearts = 1<<CardIds.ten_hearts.value
    king_hearts = 1<<CardIds.king_hearts.value
    nine_hearts = 1<<CardIds.nine_hearts.value
    eight_hearts = 1<<CardIds.eight_hearts.value
    seven_hearts = 1<<CardIds.seven_hearts.value