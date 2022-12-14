from collections import Counter
from typing import List

from cards.Card import Card, CardNumber


def sort_by_number_lt(s: List[Card], o: List[Card]) -> bool:
    return _high_card_lt(sorted([c.number for c in s], reverse=True), sorted([c.number for c in o], reverse=True))


def sort_by_occurence_lt(s: List[Card], o: List[Card]) -> bool:
    s_c, o_c = _group_and_sort_by_occurence(s), _group_and_sort_by_occurence(o)

    return _high_card_lt([t[0] for t in s_c], [t[0] for t in o_c])


def straight_lt(s: List[Card], o: List[Card]) -> bool:
    s_high, o_high = _get_straight_highest_card(s), _get_straight_highest_card(o)
    return s_high < o_high


def _get_straight_highest_card(s: List[Card]) -> CardNumber:
    numbers = sorted([c.number for c in s], reverse=True)
    if numbers[0] == CardNumber.ACE and numbers[1] == CardNumber.FIVE:
        return numbers[1]
    else:
        return numbers[0]


def _group_and_sort_by_occurence(stack: List[Card]) -> List[tuple[CardNumber, int]]:
    return sorted(Counter([c.number for c in stack]).most_common(), key=lambda t: (t[1], t[0]), reverse=True)


def _high_card_lt(s: List[CardNumber], o: List[CardNumber]) -> bool:
    for s_i, o_i in zip(s, o):
        if s_i < o_i:
            return True
        elif o_i < s_i:
            return False
    return False
