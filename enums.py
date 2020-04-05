from enum import Enum
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
    queen_clubs = 1<<CardIds.queen_clubs
    seven_diamonds = 1<<CardIds.seven_diamonds
    queen_spades = 1<<CardIds.queen_spades
    queen_hearts = 1<<CardIds.queen_hearts
    queen_diamonds = 1<<CardIds.queen_diamonds
    jack_clubs = 1<<CardIds.jack_clubs
    jack_spades = 1<<CardIds.jack_spades
    jack_hearts = 1<<CardIds.jack_hearts
    jack_diamonds = 1<<CardIds.jack_diamonds
    ace_diamonds = 1<<CardIds.ace_diamonds
    ten_diamonds = 1<<CardIds.ten_diamonds
    king_diamonds = 1<<CardIds.king_diamonds
    nine_diamonds = 1<<CardIds.nine_diamonds
    eight_diamonds = 1<<CardIds.eight_diamonds
    ace_clubs = 1<<CardIds.ace_clubs
    ten_clubs = 1<<CardIds.ten_clubs
    king_clubs = 1<<CardIds.king_clubs
    nine_clubs = 1<<CardIds.nine_clubs
    eight_clubs = 1<<CardIds.eight_clubs
    seven_clubs = 1<<CardIds.seven_clubs
    ace_spades = 1<<CardIds.ace_spades
    ten_spades = 1<<CardIds.ten_spades
    king_spades = 1<<CardIds.king_spades
    nine_spades = 1<<CardIds.nine_spades
    eight_spades = 1<<CardIds.eight_spades
    seven_spades = 1<<CardIds.seven_spades
    ace_hearts = 1<<CardIds.ace_hearts
    ten_hearts = 1<<CardIds.ten_hearts
    king_hearts = 1<<CardIds.king_hearts
    nine_hearts = 1<<CardIds.nine_hearts
    eight_hearts = 1<<CardIds.eight_hearts
    seven_hearts = 1<<CardIds.seven_hearts