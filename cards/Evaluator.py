from collections import Counter
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


class EvaluatorOf5Cards:
    def __init__(self, cards: List[Card]):
        self.card_number = 5
        assert len(cards) == self.card_number, f"Must be {self.card_number} cards"
        self.original_cards = cards

    def getOptimalCards(self):
        pass

    def is_flush(self) -> bool:
        genre = self.original_cards[0].genre
        return all(c.genre == genre for c in self.original_cards)

    def is_straight(self) -> bool:
        numbers = sorted(list(set(c.number.value for c in self.original_cards)))
        n = len(numbers)
        if n < 5:
            return False

        return all(numbers[i + 1] - numbers[i] == 1 for i in range(n - 1)) or (  # ascending by 1
            all(numbers[i + 1] - numbers[i] == 1 for i in range(n - 2))
            and numbers[0] == 2
            and numbers[4] == 14  # 2345A
        )

    def is_straight_flush(self) -> bool:
        return self.is_flush() and self.is_straight()

    def is_royal_straight_flush(self) -> bool:
        return self.is_straight_flush() and (
            [10, 11, 12, 13, 14] == sorted(list(set(c.number.value for c in self.original_cards)))
        )

    def is_four_of_a_kind(self) -> bool:
        return self._group_by_numbers() == [4, 1]

    def is_full_house(self) -> bool:
        return self._group_by_numbers() == [3, 2]

    def is_three_of_a_kind(self) -> bool:
        return self._group_by_numbers() == [3, 1, 1]

    def _group_by_numbers(self) -> List[int]:
        c = Counter([c.number.value for c in self.original_cards])
        return [t[1] for t in c.most_common()]


class EvaluatorOf7Cards:
    def __init__(self, cards: List[Card]):
        assert len(cards) == NUMBER_OF_CARDS, f"Must be {NUMBER_OF_CARDS}"
        self.original_cards = cards

    def getOptimalCards(self):
        pass

    @staticmethod
    def has_flush(cards: List[Card]) -> bool:
        groups = {}
        for card in cards:
            lst = groups.get(card.genre, [])
            lst.append(card)
            groups[card.genre] = lst

        return any(len(val) >= 5 for _, val in groups.items())

    @staticmethod
    def has_straight(cards: List[Card]) -> bool:
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
    def has_four_of_kind(cards: List[Card]) -> bool:
        groups = {}
        for card in cards:
            lst = groups.get(card.number, [])
            lst.append(card)
            groups[card.number] = lst

        return any(len(val) == 4 for _, val in groups.items())
