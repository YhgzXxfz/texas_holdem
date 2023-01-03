import random
from typing import List

from cards.Card import Card, CardNumber, Genre


class Deck:
    def __init__(self) -> None:
        self.cards = self._generate_cards()
        self.index = 0

    def _generate_cards(self) -> List[Card]:
        cards = [Card(g, n) for g in Genre for n in CardNumber]
        random.shuffle(cards)
        return cards

    def skip_one_card(self) -> None:
        self.index += 1

    def peek_top_card(self) -> Card:
        if self.index > len(self.cards):
            raise IndexError
        return self.cards[self.index]

    def pop_cards(self, n: int = 1):
        if self.index + n > len(self.cards):
            raise IndexError
        result = self.cards[self.index : self.index + n]
        self.index += n
        return tuple(result)
