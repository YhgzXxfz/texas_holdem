from enum import Enum


class Evaluation(Enum):
    HIGH_CARD = 1
    ONE_PAIR = 2
    TWO_PAIRS = 3
    THREE_OF_A_KIND = 4
    STRAIGHT = 5
    FLUSH = 6
    FULL_HOUSE = 7
    FOUR_OF_A_KIND = 8
    STRAIGHT_FLUSH = 9
    ROYAL_STRAIGHT_FLUSH = 10

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented
