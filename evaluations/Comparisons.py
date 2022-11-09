from typing import List

from cards.Card import Card


def single_card_lt(s: Card, o: Card) -> bool:
    return s.number < o.number


def high_card_lt(s: List[Card], o: List[Card]) -> bool:
    s.sort(key=lambda c: c.number, reverse=True)
    o.sort(key=lambda c: c.number, reverse=True)
    for s_i, o_i in zip(s, o):
        if single_card_lt(s_i, o_i):
            return True
        elif single_card_lt(o_i, s_i):
            return False
    return False
