from enum import Enum


class Genre(Enum):
    SPADE = 0
    HEART = 1
    CLUB = 2
    DIAMOND = 3

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented


class CardNumber(Enum):
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented


class Card:
    def __init__(self, genre: Genre, number: CardNumber):
        self.genre = genre
        self.number = number

    def __str__(self) -> str:
        return f"{self.genre} {self.number}"

    def __lt__(self, o: object) -> bool:
        if self.__class__ is not o.__class__:
            return NotImplemented
        if self.genre == o.genre:
            return self.number < o.number
        else:
            return self.genre < o.genre

    def __eq__(self, o: object) -> bool:
        if self.__class__ is o.__class__:
            return self.genre == o.genre and self.number == o.number
        return NotImplemented

    def __hash__(self) -> int:
        return hash((self.genre, self.number))
