import unittest
from typing import List

from unittest_data_provider import data_provider

from cards.Card import Card, CardNumber, Genre
from evaluations.Evaluation import Evaluation
from evaluations.EvaluatorOf5Cards import EvaluatorOf5Cards


class TestEvaluationOf5Cards(unittest.TestCase):
    def setUp(self) -> None:
        self.royal_straight_flush = [
            Card(Genre.DIAMOND, CardNumber.QUEEN),
            Card(Genre.DIAMOND, CardNumber.ACE),
            Card(Genre.DIAMOND, CardNumber.KING),
            Card(Genre.DIAMOND, CardNumber.TEN),
            Card(Genre.DIAMOND, CardNumber.JACK),
        ]
        self.straight_flush = [
            Card(Genre.DIAMOND, CardNumber.QUEEN),
            Card(Genre.DIAMOND, CardNumber.NINE),
            Card(Genre.DIAMOND, CardNumber.KING),
            Card(Genre.DIAMOND, CardNumber.TEN),
            Card(Genre.DIAMOND, CardNumber.JACK),
        ]
        self.four_of_a_kind = [
            Card(Genre.DIAMOND, CardNumber.QUEEN),
            Card(Genre.SPADE, CardNumber.QUEEN),
            Card(Genre.CLUB, CardNumber.QUEEN),
            Card(Genre.HEART, CardNumber.QUEEN),
            Card(Genre.CLUB, CardNumber.JACK),
        ]
        self.full_house = [
            Card(Genre.DIAMOND, CardNumber.QUEEN),
            Card(Genre.SPADE, CardNumber.QUEEN),
            Card(Genre.CLUB, CardNumber.QUEEN),
            Card(Genre.HEART, CardNumber.JACK),
            Card(Genre.CLUB, CardNumber.JACK),
        ]
        self.flush = [
            Card(Genre.DIAMOND, CardNumber.QUEEN),
            Card(Genre.DIAMOND, CardNumber.ACE),
            Card(Genre.DIAMOND, CardNumber.KING),
            Card(Genre.DIAMOND, CardNumber.EIGHT),
            Card(Genre.DIAMOND, CardNumber.JACK),
        ]
        self.straight = [
            Card(Genre.DIAMOND, CardNumber.TWO),
            Card(Genre.SPADE, CardNumber.ACE),
            Card(Genre.SPADE, CardNumber.THREE),
            Card(Genre.HEART, CardNumber.FOUR),
            Card(Genre.CLUB, CardNumber.FIVE),
        ]
        self.three_of_a_kind = [
            Card(Genre.DIAMOND, CardNumber.QUEEN),
            Card(Genre.SPADE, CardNumber.QUEEN),
            Card(Genre.CLUB, CardNumber.QUEEN),
            Card(Genre.HEART, CardNumber.JACK),
            Card(Genre.CLUB, CardNumber.TEN),
        ]
        self.two_pairs = [
            Card(Genre.DIAMOND, CardNumber.QUEEN),
            Card(Genre.SPADE, CardNumber.QUEEN),
            Card(Genre.CLUB, CardNumber.JACK),
            Card(Genre.HEART, CardNumber.JACK),
            Card(Genre.CLUB, CardNumber.TEN),
        ]
        self.one_pair = [
            Card(Genre.DIAMOND, CardNumber.QUEEN),
            Card(Genre.SPADE, CardNumber.QUEEN),
            Card(Genre.CLUB, CardNumber.JACK),
            Card(Genre.HEART, CardNumber.ACE),
            Card(Genre.CLUB, CardNumber.TEN),
        ]
        self.high_card = [
            Card(Genre.DIAMOND, CardNumber.QUEEN),
            Card(Genre.SPADE, CardNumber.TWO),
            Card(Genre.CLUB, CardNumber.JACK),
            Card(Genre.HEART, CardNumber.ACE),
            Card(Genre.CLUB, CardNumber.TEN),
        ]
        return super().setUp()

    @data_provider(
        lambda: (
            (
                [
                    Card(Genre.DIAMOND, CardNumber.QUEEN),
                    Card(Genre.SPADE, CardNumber.ACE),
                    Card(Genre.SPADE, CardNumber.KING),
                    Card(Genre.HEART, CardNumber.EIGHT),
                    Card(Genre.CLUB, CardNumber.JACK),
                ],
                False,
            ),
            (
                [
                    Card(Genre.DIAMOND, CardNumber.QUEEN),
                    Card(Genre.DIAMOND, CardNumber.ACE),
                    Card(Genre.DIAMOND, CardNumber.KING),
                    Card(Genre.DIAMOND, CardNumber.EIGHT),
                    Card(Genre.DIAMOND, CardNumber.JACK),
                ],
                True,
            ),
        )
    )
    def test_is_flush(self, stack: List[Card], is_flush: bool):
        e = EvaluatorOf5Cards(stack)
        self.assertEqual(e.is_flush(), is_flush)

    @data_provider(
        lambda: (
            (
                [
                    Card(Genre.DIAMOND, CardNumber.QUEEN),
                    Card(Genre.SPADE, CardNumber.ACE),
                    Card(Genre.SPADE, CardNumber.KING),
                    Card(Genre.HEART, CardNumber.EIGHT),
                    Card(Genre.CLUB, CardNumber.JACK),
                ],
                False,
            ),
            (
                [
                    Card(Genre.DIAMOND, CardNumber.QUEEN),
                    Card(Genre.SPADE, CardNumber.ACE),
                    Card(Genre.SPADE, CardNumber.KING),
                    Card(Genre.HEART, CardNumber.TEN),
                    Card(Genre.CLUB, CardNumber.JACK),
                ],
                True,
            ),
            (
                [
                    Card(Genre.DIAMOND, CardNumber.TWO),
                    Card(Genre.SPADE, CardNumber.ACE),
                    Card(Genre.SPADE, CardNumber.THREE),
                    Card(Genre.HEART, CardNumber.FOUR),
                    Card(Genre.CLUB, CardNumber.FIVE),
                ],
                True,
            ),
        )
    )
    def test_is_straight(self, stack: List[Card], is_straight: bool):
        # Not a straight
        e = EvaluatorOf5Cards(stack)
        self.assertEqual(e.is_straight(), is_straight)

    @data_provider(
        lambda: (
            (
                [
                    # staight but not flush
                    Card(Genre.DIAMOND, CardNumber.QUEEN),
                    Card(Genre.SPADE, CardNumber.ACE),
                    Card(Genre.SPADE, CardNumber.KING),
                    Card(Genre.HEART, CardNumber.TEN),
                    Card(Genre.CLUB, CardNumber.JACK),
                ],
                False,
            ),
            (
                [
                    # flush but not straight
                    Card(Genre.DIAMOND, CardNumber.QUEEN),
                    Card(Genre.DIAMOND, CardNumber.ACE),
                    Card(Genre.DIAMOND, CardNumber.KING),
                    Card(Genre.DIAMOND, CardNumber.NINE),
                    Card(Genre.DIAMOND, CardNumber.JACK),
                ],
                False,
            ),
            (
                [
                    Card(Genre.DIAMOND, CardNumber.QUEEN),
                    Card(Genre.DIAMOND, CardNumber.ACE),
                    Card(Genre.DIAMOND, CardNumber.KING),
                    Card(Genre.DIAMOND, CardNumber.TEN),
                    Card(Genre.DIAMOND, CardNumber.JACK),
                ],
                True,
            ),
        )
    )
    def test_is_straight_flush(self, stack: List[Card], is_straight_flush: bool):
        e = EvaluatorOf5Cards(stack)
        self.assertEqual(e.is_straight_flush(), is_straight_flush)

    @data_provider(
        lambda: (
            (
                [
                    Card(Genre.DIAMOND, CardNumber.QUEEN),
                    Card(Genre.DIAMOND, CardNumber.ACE),
                    Card(Genre.DIAMOND, CardNumber.KING),
                    Card(Genre.DIAMOND, CardNumber.TEN),
                    Card(Genre.DIAMOND, CardNumber.JACK),
                ],
                True,
            ),
            (
                [
                    Card(Genre.DIAMOND, CardNumber.QUEEN),
                    Card(Genre.DIAMOND, CardNumber.NINE),
                    Card(Genre.DIAMOND, CardNumber.KING),
                    Card(Genre.DIAMOND, CardNumber.TEN),
                    Card(Genre.DIAMOND, CardNumber.JACK),
                ],
                False,
            ),
            (
                [
                    Card(Genre.DIAMOND, CardNumber.ACE),
                    Card(Genre.DIAMOND, CardNumber.TWO),
                    Card(Genre.DIAMOND, CardNumber.THREE),
                    Card(Genre.DIAMOND, CardNumber.FOUR),
                    Card(Genre.DIAMOND, CardNumber.FIVE),
                ],
                False,
            ),
        )
    )
    def test_is_royal_straight_flush(self, stack: List[Card], is_royal_straight_flush: bool):
        e = EvaluatorOf5Cards(stack)
        self.assertEqual(e.is_royal_straight_flush(), is_royal_straight_flush)

    @data_provider(
        lambda: (
            (
                [
                    Card(Genre.DIAMOND, CardNumber.QUEEN),
                    Card(Genre.SPADE, CardNumber.QUEEN),
                    Card(Genre.CLUB, CardNumber.QUEEN),
                    Card(Genre.HEART, CardNumber.QUEEN),
                    Card(Genre.CLUB, CardNumber.JACK),
                ],
                True,
            ),
            (
                [
                    Card(Genre.DIAMOND, CardNumber.QUEEN),
                    Card(Genre.SPADE, CardNumber.QUEEN),
                    Card(Genre.CLUB, CardNumber.QUEEN),
                    Card(Genre.HEART, CardNumber.JACK),
                    Card(Genre.CLUB, CardNumber.JACK),
                ],
                False,
            ),
        )
    )
    def test_is_four_of_a_kind(self, stack: List[Card], is_four_of_a_kind: bool):
        e = EvaluatorOf5Cards(stack)
        self.assertEqual(e.is_four_of_a_kind(), is_four_of_a_kind)

    @data_provider(
        lambda: (
            (
                [
                    Card(Genre.DIAMOND, CardNumber.QUEEN),
                    Card(Genre.SPADE, CardNumber.QUEEN),
                    Card(Genre.CLUB, CardNumber.QUEEN),
                    Card(Genre.HEART, CardNumber.QUEEN),
                    Card(Genre.CLUB, CardNumber.JACK),
                ],
                False,
            ),
            (
                [
                    Card(Genre.DIAMOND, CardNumber.QUEEN),
                    Card(Genre.SPADE, CardNumber.QUEEN),
                    Card(Genre.CLUB, CardNumber.QUEEN),
                    Card(Genre.HEART, CardNumber.JACK),
                    Card(Genre.CLUB, CardNumber.TEN),
                ],
                False,
            ),
            (
                [
                    Card(Genre.DIAMOND, CardNumber.QUEEN),
                    Card(Genre.SPADE, CardNumber.QUEEN),
                    Card(Genre.CLUB, CardNumber.JACK),
                    Card(Genre.HEART, CardNumber.JACK),
                    Card(Genre.CLUB, CardNumber.TEN),
                ],
                False,
            ),
            (
                [
                    Card(Genre.DIAMOND, CardNumber.QUEEN),
                    Card(Genre.SPADE, CardNumber.QUEEN),
                    Card(Genre.CLUB, CardNumber.QUEEN),
                    Card(Genre.HEART, CardNumber.JACK),
                    Card(Genre.CLUB, CardNumber.JACK),
                ],
                True,
            ),
        )
    )
    def test_is_full_house(self, stack: List[Card], is_full_house: bool):
        e = EvaluatorOf5Cards(stack)
        self.assertEqual(e.is_full_house(), is_full_house)

    @data_provider(
        lambda: (
            (
                [
                    Card(Genre.DIAMOND, CardNumber.QUEEN),
                    Card(Genre.SPADE, CardNumber.QUEEN),
                    Card(Genre.CLUB, CardNumber.QUEEN),
                    Card(Genre.HEART, CardNumber.QUEEN),
                    Card(Genre.CLUB, CardNumber.JACK),
                ],
                False,
            ),
            (
                [
                    Card(Genre.DIAMOND, CardNumber.QUEEN),
                    Card(Genre.SPADE, CardNumber.QUEEN),
                    Card(Genre.CLUB, CardNumber.QUEEN),
                    Card(Genre.HEART, CardNumber.JACK),
                    Card(Genre.CLUB, CardNumber.JACK),
                ],
                False,
            ),
            (
                [
                    Card(Genre.DIAMOND, CardNumber.QUEEN),
                    Card(Genre.SPADE, CardNumber.QUEEN),
                    Card(Genre.CLUB, CardNumber.JACK),
                    Card(Genre.HEART, CardNumber.JACK),
                    Card(Genre.CLUB, CardNumber.TEN),
                ],
                False,
            ),
            (
                [
                    Card(Genre.DIAMOND, CardNumber.QUEEN),
                    Card(Genre.SPADE, CardNumber.QUEEN),
                    Card(Genre.CLUB, CardNumber.QUEEN),
                    Card(Genre.HEART, CardNumber.JACK),
                    Card(Genre.CLUB, CardNumber.TEN),
                ],
                True,
            ),
        )
    )
    def test_is_three_of_a_kind(self, stack: List[Card], is_three_of_a_kind: bool):
        e = EvaluatorOf5Cards(stack)
        self.assertEqual(e.is_three_of_a_kind(), is_three_of_a_kind)

    @data_provider(
        lambda: (
            (
                [
                    Card(Genre.DIAMOND, CardNumber.QUEEN),
                    Card(Genre.SPADE, CardNumber.QUEEN),
                    Card(Genre.CLUB, CardNumber.QUEEN),
                    Card(Genre.HEART, CardNumber.QUEEN),
                    Card(Genre.CLUB, CardNumber.JACK),
                ],
                False,
            ),
            (
                [
                    Card(Genre.DIAMOND, CardNumber.QUEEN),
                    Card(Genre.SPADE, CardNumber.QUEEN),
                    Card(Genre.CLUB, CardNumber.QUEEN),
                    Card(Genre.HEART, CardNumber.JACK),
                    Card(Genre.CLUB, CardNumber.JACK),
                ],
                False,
            ),
            (
                [
                    Card(Genre.DIAMOND, CardNumber.QUEEN),
                    Card(Genre.SPADE, CardNumber.QUEEN),
                    Card(Genre.CLUB, CardNumber.QUEEN),
                    Card(Genre.HEART, CardNumber.JACK),
                    Card(Genre.CLUB, CardNumber.TEN),
                ],
                False,
            ),
            (
                [
                    Card(Genre.DIAMOND, CardNumber.QUEEN),
                    Card(Genre.SPADE, CardNumber.QUEEN),
                    Card(Genre.CLUB, CardNumber.JACK),
                    Card(Genre.HEART, CardNumber.JACK),
                    Card(Genre.CLUB, CardNumber.TEN),
                ],
                True,
            ),
        )
    )
    def test_is_two_pairs(self, stack: List[Card], is_two_pairs: bool):
        e = EvaluatorOf5Cards(stack)
        self.assertEqual(e.is_two_pairs(), is_two_pairs)

    @data_provider(
        lambda: (
            (
                [
                    Card(Genre.DIAMOND, CardNumber.QUEEN),
                    Card(Genre.SPADE, CardNumber.QUEEN),
                    Card(Genre.CLUB, CardNumber.QUEEN),
                    Card(Genre.HEART, CardNumber.QUEEN),
                    Card(Genre.CLUB, CardNumber.JACK),
                ],
                False,
            ),
            (
                [
                    Card(Genre.DIAMOND, CardNumber.QUEEN),
                    Card(Genre.SPADE, CardNumber.QUEEN),
                    Card(Genre.CLUB, CardNumber.QUEEN),
                    Card(Genre.HEART, CardNumber.JACK),
                    Card(Genre.CLUB, CardNumber.JACK),
                ],
                False,
            ),
            (
                [
                    Card(Genre.DIAMOND, CardNumber.QUEEN),
                    Card(Genre.SPADE, CardNumber.QUEEN),
                    Card(Genre.CLUB, CardNumber.QUEEN),
                    Card(Genre.HEART, CardNumber.JACK),
                    Card(Genre.CLUB, CardNumber.TEN),
                ],
                False,
            ),
            (
                [
                    Card(Genre.DIAMOND, CardNumber.QUEEN),
                    Card(Genre.SPADE, CardNumber.QUEEN),
                    Card(Genre.CLUB, CardNumber.JACK),
                    Card(Genre.HEART, CardNumber.JACK),
                    Card(Genre.CLUB, CardNumber.TEN),
                ],
                False,
            ),
            (
                [
                    Card(Genre.DIAMOND, CardNumber.QUEEN),
                    Card(Genre.SPADE, CardNumber.QUEEN),
                    Card(Genre.CLUB, CardNumber.JACK),
                    Card(Genre.HEART, CardNumber.ACE),
                    Card(Genre.CLUB, CardNumber.TEN),
                ],
                True,
            ),
        )
    )
    def test_is_one_pair(self, stack: List[Card], is_one_pair: bool):
        e = EvaluatorOf5Cards(stack)
        self.assertEqual(e.is_one_pair(), is_one_pair)

    def test_evaluation(self):
        royal_straight_flush = EvaluatorOf5Cards(self.royal_straight_flush)
        self.assertEqual(royal_straight_flush.get_evaluation(), Evaluation.ROYAL_STRAIGHT_FLUSH)

        straight_flush = EvaluatorOf5Cards(self.straight_flush)
        self.assertEqual(straight_flush.get_evaluation(), Evaluation.STRAIGHT_FLUSH)

        four_of_a_kind = EvaluatorOf5Cards(self.four_of_a_kind)
        self.assertEqual(four_of_a_kind.get_evaluation(), Evaluation.FOUR_OF_A_KIND)

        full_house = EvaluatorOf5Cards(self.full_house)
        self.assertEqual(full_house.get_evaluation(), Evaluation.FULL_HOUSE)

        flush = EvaluatorOf5Cards(self.flush)
        self.assertEqual(flush.get_evaluation(), Evaluation.FLUSH)

        straight = EvaluatorOf5Cards(self.straight)
        self.assertEqual(straight.get_evaluation(), Evaluation.STRAIGHT)

        three_of_a_kind = EvaluatorOf5Cards(self.three_of_a_kind)
        self.assertEqual(three_of_a_kind.get_evaluation(), Evaluation.THREE_OF_A_KIND)

        two_pairs = EvaluatorOf5Cards(self.two_pairs)
        self.assertEqual(two_pairs.get_evaluation(), Evaluation.TWO_PAIRS)

        one_pair = EvaluatorOf5Cards(self.one_pair)
        self.assertEqual(one_pair.get_evaluation(), Evaluation.ONE_PAIR)

        high_card = EvaluatorOf5Cards(self.high_card)
        self.assertEqual(high_card.get_evaluation(), Evaluation.HIGH_CARD)

    def test_comparison_when_evaluations_are_different(self):
        royal_straight_flush = EvaluatorOf5Cards(self.royal_straight_flush)
        straight_flush = EvaluatorOf5Cards(self.straight_flush)
        four_of_a_kind = EvaluatorOf5Cards(self.four_of_a_kind)
        full_house = EvaluatorOf5Cards(self.full_house)
        flush = EvaluatorOf5Cards(self.flush)
        straight = EvaluatorOf5Cards(self.straight)
        three_of_a_kind = EvaluatorOf5Cards(self.three_of_a_kind)
        two_pairs = EvaluatorOf5Cards(self.two_pairs)
        one_pair = EvaluatorOf5Cards(self.one_pair)
        high_card = EvaluatorOf5Cards(self.high_card)

        self.assertTrue(high_card < one_pair)
        self.assertTrue(one_pair < two_pairs)
        self.assertTrue(two_pairs < three_of_a_kind)
        self.assertTrue(three_of_a_kind < straight)
        self.assertTrue(straight < flush)
        self.assertTrue(flush < full_house)
        self.assertTrue(full_house < four_of_a_kind)
        self.assertTrue(four_of_a_kind < straight_flush)
        self.assertTrue(straight_flush < royal_straight_flush)

    @data_provider(
        lambda: (
            # High Card
            (
                [
                    # AQT92
                    Card(Genre.DIAMOND, CardNumber.QUEEN),
                    Card(Genre.SPADE, CardNumber.TWO),
                    Card(Genre.DIAMOND, CardNumber.NINE),
                    Card(Genre.HEART, CardNumber.ACE),
                    Card(Genre.CLUB, CardNumber.TEN),
                ],
                [
                    # AQJ62
                    Card(Genre.DIAMOND, CardNumber.QUEEN),
                    Card(Genre.SPADE, CardNumber.TWO),
                    Card(Genre.CLUB, CardNumber.JACK),
                    Card(Genre.HEART, CardNumber.ACE),
                    Card(Genre.CLUB, CardNumber.SIX),
                ],
                Evaluation.HIGH_CARD,
            ),
            # One Pair
            (
                [
                    # JJAQ2
                    Card(Genre.DIAMOND, CardNumber.QUEEN),
                    Card(Genre.SPADE, CardNumber.TWO),
                    Card(Genre.SPADE, CardNumber.JACK),
                    Card(Genre.HEART, CardNumber.ACE),
                    Card(Genre.CLUB, CardNumber.JACK),
                ],
                [
                    # QQAT2
                    Card(Genre.HEART, CardNumber.QUEEN),
                    Card(Genre.SPADE, CardNumber.TWO),
                    Card(Genre.DIAMOND, CardNumber.QUEEN),
                    Card(Genre.HEART, CardNumber.ACE),
                    Card(Genre.CLUB, CardNumber.TEN),
                ],
                Evaluation.ONE_PAIR,
            ),
            (
                [
                    # JJAT2
                    Card(Genre.HEART, CardNumber.JACK),
                    Card(Genre.SPADE, CardNumber.TWO),
                    Card(Genre.DIAMOND, CardNumber.JACK),
                    Card(Genre.HEART, CardNumber.ACE),
                    Card(Genre.CLUB, CardNumber.TEN),
                ],
                [
                    # JJAQ2
                    Card(Genre.DIAMOND, CardNumber.QUEEN),
                    Card(Genre.SPADE, CardNumber.TWO),
                    Card(Genre.SPADE, CardNumber.JACK),
                    Card(Genre.HEART, CardNumber.ACE),
                    Card(Genre.CLUB, CardNumber.JACK),
                ],
                Evaluation.ONE_PAIR,
            ),
            # two pairs
            (
                [
                    # JJAT2
                    Card(Genre.DIAMOND, CardNumber.QUEEN),
                    Card(Genre.SPADE, CardNumber.ACE),
                    Card(Genre.SPADE, CardNumber.JACK),
                    Card(Genre.HEART, CardNumber.QUEEN),
                    Card(Genre.CLUB, CardNumber.JACK),
                ],
                [
                    # JJAQ2
                    Card(Genre.HEART, CardNumber.QUEEN),
                    Card(Genre.SPADE, CardNumber.TWO),
                    Card(Genre.DIAMOND, CardNumber.ACE),
                    Card(Genre.HEART, CardNumber.ACE),
                    Card(Genre.CLUB, CardNumber.TWO),
                ],
                Evaluation.TWO_PAIRS,
            ),
            (
                [
                    # JJ66A
                    Card(Genre.HEART, CardNumber.JACK),
                    Card(Genre.SPADE, CardNumber.SIX),
                    Card(Genre.DIAMOND, CardNumber.JACK),
                    Card(Genre.HEART, CardNumber.ACE),
                    Card(Genre.CLUB, CardNumber.SIX),
                ],
                [
                    # JJTTK
                    Card(Genre.DIAMOND, CardNumber.TEN),
                    Card(Genre.SPADE, CardNumber.KING),
                    Card(Genre.SPADE, CardNumber.JACK),
                    Card(Genre.HEART, CardNumber.TEN),
                    Card(Genre.CLUB, CardNumber.JACK),
                ],
                Evaluation.TWO_PAIRS,
            ),
            (
                [
                    # JJTTK
                    Card(Genre.DIAMOND, CardNumber.TEN),
                    Card(Genre.SPADE, CardNumber.KING),
                    Card(Genre.SPADE, CardNumber.JACK),
                    Card(Genre.HEART, CardNumber.TEN),
                    Card(Genre.CLUB, CardNumber.JACK),
                ],
                [
                    # JJTTA
                    Card(Genre.HEART, CardNumber.JACK),
                    Card(Genre.SPADE, CardNumber.TEN),
                    Card(Genre.DIAMOND, CardNumber.JACK),
                    Card(Genre.HEART, CardNumber.ACE),
                    Card(Genre.CLUB, CardNumber.TEN),
                ],
                Evaluation.TWO_PAIRS,
            ),
            # Three of a kind
            (
                [
                    # QQQA6
                    Card(Genre.DIAMOND, CardNumber.QUEEN),
                    Card(Genre.SPADE, CardNumber.QUEEN),
                    Card(Genre.SPADE, CardNumber.SIX),
                    Card(Genre.HEART, CardNumber.QUEEN),
                    Card(Genre.CLUB, CardNumber.ACE),
                ],
                [
                    # KKKJ6
                    Card(Genre.DIAMOND, CardNumber.KING),
                    Card(Genre.SPADE, CardNumber.KING),
                    Card(Genre.SPADE, CardNumber.SIX),
                    Card(Genre.HEART, CardNumber.KING),
                    Card(Genre.CLUB, CardNumber.JACK),
                ],
                Evaluation.THREE_OF_A_KIND,
            ),
            (
                [
                    # QQQJ6
                    Card(Genre.DIAMOND, CardNumber.QUEEN),
                    Card(Genre.SPADE, CardNumber.QUEEN),
                    Card(Genre.SPADE, CardNumber.SIX),
                    Card(Genre.HEART, CardNumber.QUEEN),
                    Card(Genre.CLUB, CardNumber.JACK),
                ],
                [
                    # QQQA5
                    Card(Genre.DIAMOND, CardNumber.QUEEN),
                    Card(Genre.SPADE, CardNumber.QUEEN),
                    Card(Genre.SPADE, CardNumber.FIVE),
                    Card(Genre.HEART, CardNumber.QUEEN),
                    Card(Genre.CLUB, CardNumber.ACE),
                ],
                Evaluation.THREE_OF_A_KIND,
            ),
            # full house
            (
                [
                    # TTTAA
                    Card(Genre.DIAMOND, CardNumber.TEN),
                    Card(Genre.SPADE, CardNumber.TEN),
                    Card(Genre.SPADE, CardNumber.ACE),
                    Card(Genre.HEART, CardNumber.TEN),
                    Card(Genre.CLUB, CardNumber.ACE),
                ],
                [
                    # QQQJJ
                    Card(Genre.DIAMOND, CardNumber.QUEEN),
                    Card(Genre.SPADE, CardNumber.QUEEN),
                    Card(Genre.SPADE, CardNumber.JACK),
                    Card(Genre.HEART, CardNumber.QUEEN),
                    Card(Genre.CLUB, CardNumber.JACK),
                ],
                Evaluation.FULL_HOUSE,
            ),
            (
                [
                    # TTTKK
                    Card(Genre.DIAMOND, CardNumber.TEN),
                    Card(Genre.SPADE, CardNumber.TEN),
                    Card(Genre.SPADE, CardNumber.KING),
                    Card(Genre.HEART, CardNumber.TEN),
                    Card(Genre.CLUB, CardNumber.KING),
                ],
                [
                    # TTTAA
                    Card(Genre.DIAMOND, CardNumber.TEN),
                    Card(Genre.SPADE, CardNumber.TEN),
                    Card(Genre.SPADE, CardNumber.ACE),
                    Card(Genre.HEART, CardNumber.TEN),
                    Card(Genre.CLUB, CardNumber.ACE),
                ],
                Evaluation.FULL_HOUSE,
            ),
            # Four of a kind
            (
                [
                    # QQQQJ
                    Card(Genre.DIAMOND, CardNumber.QUEEN),
                    Card(Genre.SPADE, CardNumber.QUEEN),
                    Card(Genre.SPADE, CardNumber.JACK),
                    Card(Genre.HEART, CardNumber.QUEEN),
                    Card(Genre.CLUB, CardNumber.QUEEN),
                ],
                [
                    # KKKK7
                    Card(Genre.DIAMOND, CardNumber.KING),
                    Card(Genre.SPADE, CardNumber.KING),
                    Card(Genre.SPADE, CardNumber.SEVEN),
                    Card(Genre.HEART, CardNumber.KING),
                    Card(Genre.CLUB, CardNumber.KING),
                ],
                Evaluation.FOUR_OF_A_KIND,
            ),
            (
                [
                    # QQQQ7
                    Card(Genre.DIAMOND, CardNumber.QUEEN),
                    Card(Genre.SPADE, CardNumber.QUEEN),
                    Card(Genre.SPADE, CardNumber.SEVEN),
                    Card(Genre.HEART, CardNumber.QUEEN),
                    Card(Genre.CLUB, CardNumber.QUEEN),
                ],
                [
                    # QQQQJ
                    Card(Genre.DIAMOND, CardNumber.QUEEN),
                    Card(Genre.SPADE, CardNumber.QUEEN),
                    Card(Genre.SPADE, CardNumber.JACK),
                    Card(Genre.HEART, CardNumber.QUEEN),
                    Card(Genre.CLUB, CardNumber.QUEEN),
                ],
                Evaluation.FOUR_OF_A_KIND,
            ),
            # Staight
            (
                [
                    # 9TJQK
                    Card(Genre.DIAMOND, CardNumber.KING),
                    Card(Genre.SPADE, CardNumber.QUEEN),
                    Card(Genre.SPADE, CardNumber.JACK),
                    Card(Genre.HEART, CardNumber.TEN),
                    Card(Genre.CLUB, CardNumber.NINE),
                ],
                [
                    # TJQKA
                    Card(Genre.DIAMOND, CardNumber.KING),
                    Card(Genre.SPADE, CardNumber.QUEEN),
                    Card(Genre.SPADE, CardNumber.JACK),
                    Card(Genre.HEART, CardNumber.TEN),
                    Card(Genre.CLUB, CardNumber.ACE),
                ],
                Evaluation.STRAIGHT,
            ),
            (
                [
                    # 12345
                    Card(Genre.DIAMOND, CardNumber.TWO),
                    Card(Genre.SPADE, CardNumber.THREE),
                    Card(Genre.SPADE, CardNumber.FOUR),
                    Card(Genre.HEART, CardNumber.FIVE),
                    Card(Genre.CLUB, CardNumber.ACE),
                ],
                [
                    # 23456
                    Card(Genre.DIAMOND, CardNumber.TWO),
                    Card(Genre.SPADE, CardNumber.THREE),
                    Card(Genre.SPADE, CardNumber.FOUR),
                    Card(Genre.HEART, CardNumber.FIVE),
                    Card(Genre.CLUB, CardNumber.SIX),
                ],
                Evaluation.STRAIGHT,
            ),
            # Flush
            (
                [
                    # K high flush
                    Card(Genre.DIAMOND, CardNumber.KING),
                    Card(Genre.DIAMOND, CardNumber.QUEEN),
                    Card(Genre.DIAMOND, CardNumber.TWO),
                    Card(Genre.DIAMOND, CardNumber.TEN),
                    Card(Genre.DIAMOND, CardNumber.NINE),
                ],
                [
                    # A high flush
                    Card(Genre.DIAMOND, CardNumber.THREE),
                    Card(Genre.DIAMOND, CardNumber.FOUR),
                    Card(Genre.DIAMOND, CardNumber.FIVE),
                    Card(Genre.DIAMOND, CardNumber.SIX),
                    Card(Genre.DIAMOND, CardNumber.ACE),
                ],
                Evaluation.FLUSH,
            ),
            # Straight flush
            (
                [
                    # 34567
                    Card(Genre.SPADE, CardNumber.THREE),
                    Card(Genre.SPADE, CardNumber.FOUR),
                    Card(Genre.SPADE, CardNumber.FIVE),
                    Card(Genre.SPADE, CardNumber.SIX),
                    Card(Genre.SPADE, CardNumber.SEVEN),
                ],
                [
                    # 9TJQK
                    Card(Genre.DIAMOND, CardNumber.KING),
                    Card(Genre.DIAMOND, CardNumber.QUEEN),
                    Card(Genre.DIAMOND, CardNumber.JACK),
                    Card(Genre.DIAMOND, CardNumber.TEN),
                    Card(Genre.DIAMOND, CardNumber.NINE),
                ],
                Evaluation.STRAIGHT_FLUSH,
            ),
            (
                [
                    # 12345
                    Card(Genre.DIAMOND, CardNumber.ACE),
                    Card(Genre.DIAMOND, CardNumber.TWO),
                    Card(Genre.DIAMOND, CardNumber.THREE),
                    Card(Genre.DIAMOND, CardNumber.FOUR),
                    Card(Genre.DIAMOND, CardNumber.FIVE),
                ],
                [
                    # 56789
                    Card(Genre.SPADE, CardNumber.FIVE),
                    Card(Genre.SPADE, CardNumber.SIX),
                    Card(Genre.SPADE, CardNumber.SEVEN),
                    Card(Genre.SPADE, CardNumber.EIGHT),
                    Card(Genre.SPADE, CardNumber.NINE),
                ],
                Evaluation.STRAIGHT_FLUSH,
            ),
            # Royal Straight Flush
            (
                [
                    Card(Genre.DIAMOND, CardNumber.ACE),
                    Card(Genre.DIAMOND, CardNumber.KING),
                    Card(Genre.DIAMOND, CardNumber.QUEEN),
                    Card(Genre.DIAMOND, CardNumber.JACK),
                    Card(Genre.DIAMOND, CardNumber.TEN),
                ],
                [
                    Card(Genre.SPADE, CardNumber.ACE),
                    Card(Genre.SPADE, CardNumber.KING),
                    Card(Genre.SPADE, CardNumber.QUEEN),
                    Card(Genre.SPADE, CardNumber.JACK),
                    Card(Genre.SPADE, CardNumber.TEN),
                ],
                Evaluation.ROYAL_STRAIGHT_FLUSH,
            ),
        )
    )
    def test_comparisons_when_evaluations_are_equal(
        self, hand_1: List[Card], hand_2: List[Card], evaluation: Evaluation
    ):
        e1 = EvaluatorOf5Cards(hand_1)
        e2 = EvaluatorOf5Cards(hand_2)
        self.assertEqual(e1.get_evaluation(), evaluation)
        self.assertEqual(e2.get_evaluation(), evaluation)

        if evaluation == Evaluation.ROYAL_STRAIGHT_FLUSH:
            self.assertTrue(e1 == e2, "royal straight flush are all equal.")
        else:
            self.assertTrue(e1 < e2)

    @data_provider(
        lambda: (
            (
                [
                    Card(Genre.SPADE, CardNumber.QUEEN),
                    Card(Genre.SPADE, CardNumber.TWO),
                    Card(Genre.DIAMOND, CardNumber.JACK),
                    Card(Genre.HEART, CardNumber.ACE),
                    Card(Genre.CLUB, CardNumber.SIX),
                ],
                [
                    Card(Genre.DIAMOND, CardNumber.QUEEN),
                    Card(Genre.SPADE, CardNumber.TWO),
                    Card(Genre.CLUB, CardNumber.JACK),
                    Card(Genre.HEART, CardNumber.ACE),
                    Card(Genre.CLUB, CardNumber.SIX),
                ],
                True,  # Same number, different suits
            ),
            (
                [
                    Card(Genre.DIAMOND, CardNumber.QUEEN),
                    Card(Genre.SPADE, CardNumber.TWO),
                    Card(Genre.CLUB, CardNumber.JACK),
                    Card(Genre.HEART, CardNumber.ACE),
                    Card(Genre.CLUB, CardNumber.SIX),
                ],
                [
                    Card(Genre.CLUB, CardNumber.JACK),
                    Card(Genre.DIAMOND, CardNumber.QUEEN),
                    Card(Genre.HEART, CardNumber.ACE),
                    Card(Genre.CLUB, CardNumber.SIX),
                    Card(Genre.SPADE, CardNumber.TWO),
                ],
                True,  # Order does not matter
            ),
            (
                [
                    Card(Genre.DIAMOND, CardNumber.QUEEN),
                    Card(Genre.SPADE, CardNumber.TWO),
                    Card(Genre.CLUB, CardNumber.JACK),
                    Card(Genre.HEART, CardNumber.ACE),
                    Card(Genre.CLUB, CardNumber.SIX),
                ],
                [
                    Card(Genre.DIAMOND, CardNumber.QUEEN),
                    Card(Genre.SPADE, CardNumber.THREE),
                    Card(Genre.CLUB, CardNumber.JACK),
                    Card(Genre.HEART, CardNumber.ACE),
                    Card(Genre.CLUB, CardNumber.SIX),
                ],
                False,
            ),
        )
    )
    def test_hashes(self, hand_1: List[Card], hand_2: List[Card], are_equal: bool) -> None:
        e1 = EvaluatorOf5Cards(hand_1)
        e2 = EvaluatorOf5Cards(hand_2)

        self.assertEqual(e1.__hash__() == e2.__hash__(), are_equal)
