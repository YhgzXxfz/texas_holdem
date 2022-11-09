from typing import List

from cards.Card import Card

NUMBER_OF_CARDS = 7


class EvaluatorOf7Cards:
    def __init__(self, cards: List[Card]):
        assert len(set(cards)) == NUMBER_OF_CARDS, f"Must be {NUMBER_OF_CARDS}"
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
