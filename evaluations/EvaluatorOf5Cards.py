from collections import Counter
from typing import List

from cards.Card import Card

from evaluations.Comparisons import sort_by_number_lt, sort_by_occurence_lt, straight_lt
from evaluations.Evaluation import Evaluation


class EvaluatorOf5Cards:
    def __init__(self, cards: List[Card]):
        self.card_number = 5
        assert len(set(cards)) == self.card_number, f"Must be {self.card_number} cards"
        self.original_cards = cards

    def getOptimalCards(self) -> Evaluation:
        if self.is_royal_straight_flush():
            return Evaluation.ROYAL_STRAIGHT_FLUSH
        elif self.is_straight_flush():
            return Evaluation.STRAIGHT_FLUSH
        elif self.is_four_of_a_kind():
            return Evaluation.FOUR_OF_A_KIND
        elif self.is_full_house():
            return Evaluation.FULL_HOUSE
        elif self.is_flush():
            return Evaluation.FLUSH
        elif self.is_straight():
            return Evaluation.STRAIGHT
        elif self.is_three_of_a_kind():
            return Evaluation.THREE_OF_A_KIND
        elif self.is_two_pairs():
            return Evaluation.TWO_PAIRS
        elif self.is_one_pair():
            return Evaluation.ONE_PAIR
        else:
            return Evaluation.HIGH_CARD

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

    def is_two_pairs(self) -> bool:
        return self._group_by_numbers() == [2, 2, 1]

    def is_one_pair(self) -> bool:
        return self._group_by_numbers() == [2, 1, 1, 1]

    def _group_by_numbers(self) -> List[int]:
        c = Counter([c.number.value for c in self.original_cards])
        return [t[1] for t in c.most_common()]

    def __lt__(self, o: object) -> bool:
        if self.__class__ is not o.__class__:
            return NotImplemented
        s_eval, o_eval = self.getOptimalCards(), o.getOptimalCards()
        if s_eval < o_eval:
            return True
        elif s_eval > o_eval:
            return False
        else:
            if s_eval in set([Evaluation.HIGH_CARD, Evaluation.FLUSH]):
                return sort_by_number_lt(self.original_cards, o.original_cards)
            elif s_eval in set(
                [
                    Evaluation.ONE_PAIR,
                    Evaluation.TWO_PAIRS,
                    Evaluation.THREE_OF_A_KIND,
                    Evaluation.FULL_HOUSE,
                    Evaluation.FOUR_OF_A_KIND,
                ]
            ):
                return sort_by_occurence_lt(self.original_cards, o.original_cards)
            else:
                return straight_lt(self.original_cards, o.original_cards)
