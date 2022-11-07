from enum import Enum
from typing import List

from cards.Card import Card

NUMBER_OF_CARDS = 7


class Evaluation(Enum):
    HIGH_CARD = 1
    PAIR = 2
    TWO_PAIRS = 3
    THREE_OF_A_KIND = 4
    STRAIGHT = 5
    FLUSH = 6
    FULL_HOUSE = 7
    FOUR_OF_A_KIND = 8
    FLUSH_STRAIGHT = 9
    ROYAL_FLUSH_STRAIGHT = 10

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented


class Evaluator:
    def __init__(self, cards: List[Card]):
        assert len(cards) == NUMBER_OF_CARDS, f"Must be {NUMBER_OF_CARDS}"
        self.original_cards = cards

    def getOptimalCards(self):
        pass

    @staticmethod
    def is_flush(cards: List[Card]) -> bool:
        groups = {}
        for card in cards:
            lst = groups.get(card.genre, [])
            lst.append(card)
            groups[card.genre] = lst

        return any(len(val) >= 5 for _, val in groups.items())

    @staticmethod
    def is_straight(cards: List[Card]) -> bool:
        numbers = sorted(list(set(c.number.value for c in cards)))
        n = len(numbers)
        if n < 5:
            return False

        def _verify_5_cards(numbers: List[int]) -> bool:
            assert len(numbers) == 5

            for i in range(len(numbers) - 1):
                if numbers[i + 1] - numbers[i] != 1:
                    return False
            return True

        for i in range(n - 4):
            if _verify_5_cards(numbers[i : i + 5]):
                return True

        if numbers[n - 1] == 14:
            if _verify_5_cards([1] + numbers[0:4]):
                return True
        return False

    @staticmethod
    def is_four_of_kind(cards: List[Card]) -> bool:
        groups = {}
        for card in cards:
            lst = groups.get(card.number, [])
            lst.append(card)
            groups[card.number] = lst

        return any(len(val) == 4 for _, val in groups.items())
