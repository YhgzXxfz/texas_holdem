from itertools import combinations
from typing import List

from cards.Card import Card

from evaluations.EvaluatorOf5Cards import EvaluatorOf5Cards

NUMBER_OF_CARDS = 7


class EvaluatorOf7Cards:
    def __init__(self, cards: List[Card]):
        assert len(set(cards)) == NUMBER_OF_CARDS, f"Must be {NUMBER_OF_CARDS}"
        self.original_cards = cards

    def getOptimalHands(self) -> EvaluatorOf5Cards:
        return max(EvaluatorOf5Cards(c) for c in combinations(self.original_cards, 5))
