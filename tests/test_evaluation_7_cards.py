import unittest
from typing import List

from unittest_data_provider import data_provider

from cards.Card import Card, CardNumber, Genre
from evaluations.Evaluation import Evaluation
from evaluations.EvaluatorOf5Cards import EvaluatorOf5Cards
from evaluations.EvaluatorOf7Cards import EvaluatorOf7Cards


class TestEvaluationOf7Cards(unittest.TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def _provide_7_card_hands():
        return (
            (
                Evaluation.FOUR_OF_A_KIND,
                [
                    Card(Genre.CLUB, CardNumber.THREE),
                    Card(Genre.HEART, CardNumber.THREE),
                    Card(Genre.DIAMOND, CardNumber.THREE),
                    Card(Genre.SPADE, CardNumber.THREE),
                    Card(Genre.CLUB, CardNumber.NINE),
                    Card(Genre.DIAMOND, CardNumber.NINE),
                    Card(Genre.CLUB, CardNumber.ACE),
                ],
                [
                    Card(Genre.CLUB, CardNumber.THREE),
                    Card(Genre.HEART, CardNumber.THREE),
                    Card(Genre.DIAMOND, CardNumber.THREE),
                    Card(Genre.SPADE, CardNumber.THREE),
                    Card(Genre.CLUB, CardNumber.ACE),
                ],
            ),
            (
                Evaluation.STRAIGHT,
                [
                    Card(Genre.CLUB, CardNumber.TWO),
                    Card(Genre.HEART, CardNumber.THREE),
                    Card(Genre.DIAMOND, CardNumber.FOUR),
                    Card(Genre.SPADE, CardNumber.FIVE),
                    Card(Genre.CLUB, CardNumber.FIVE),
                    Card(Genre.DIAMOND, CardNumber.FIVE),
                    Card(Genre.CLUB, CardNumber.ACE),
                ],
                [
                    Card(Genre.CLUB, CardNumber.TWO),
                    Card(Genre.HEART, CardNumber.THREE),
                    Card(Genre.DIAMOND, CardNumber.FOUR),
                    Card(Genre.SPADE, CardNumber.FIVE),
                    Card(Genre.CLUB, CardNumber.ACE),
                ],
            ),
            (
                Evaluation.FLUSH,
                [
                    Card(Genre.CLUB, CardNumber.TWO),
                    Card(Genre.HEART, CardNumber.THREE),
                    Card(Genre.CLUB, CardNumber.FOUR),
                    Card(Genre.SPADE, CardNumber.FIVE),
                    Card(Genre.CLUB, CardNumber.TEN),
                    Card(Genre.CLUB, CardNumber.JACK),
                    Card(Genre.CLUB, CardNumber.ACE),
                ],
                [
                    Card(Genre.CLUB, CardNumber.TWO),
                    Card(Genre.CLUB, CardNumber.TEN),
                    Card(Genre.CLUB, CardNumber.FOUR),
                    Card(Genre.CLUB, CardNumber.JACK),
                    Card(Genre.CLUB, CardNumber.ACE),
                ],
            ),
        )

    @data_provider(_provide_7_card_hands)
    def test_get_optimal_hands(self, evaluation, original_hand, optimal_hand):
        # When
        e = EvaluatorOf7Cards(original_hand)
        best = e.getOptimalHands()

        # Then
        self.assertTrue(
            best == EvaluatorOf5Cards(optimal_hand),
            msg="Best hand is quads plus an Ace high card.",
        )
        self.assertTrue(best.get_evaluation() == evaluation)
        self.assertTrue(set(optimal_hand) <= set(original_hand), msg="Best hand should be a subset of the 7 cards.")

    def _provide_7_card_hands_for_comparison():
        return (
            (
                "<",
                [
                    Card(Genre.CLUB, CardNumber.THREE),
                    Card(Genre.HEART, CardNumber.THREE),
                    Card(Genre.DIAMOND, CardNumber.THREE),
                    Card(Genre.CLUB, CardNumber.ACE),
                    Card(Genre.CLUB, CardNumber.NINE),
                    # hand
                    Card(Genre.DIAMOND, CardNumber.NINE),
                    Card(Genre.SPADE, CardNumber.NINE),
                ],
                [
                    Card(Genre.CLUB, CardNumber.THREE),
                    Card(Genre.HEART, CardNumber.THREE),
                    Card(Genre.DIAMOND, CardNumber.THREE),
                    Card(Genre.CLUB, CardNumber.ACE),
                    Card(Genre.CLUB, CardNumber.NINE),
                    # hand
                    Card(Genre.SPADE, CardNumber.THREE),
                    Card(Genre.DIAMOND, CardNumber.TEN),
                ],
            ),
            (
                "=",
                [
                    Card(Genre.CLUB, CardNumber.THREE),
                    Card(Genre.HEART, CardNumber.THREE),
                    Card(Genre.DIAMOND, CardNumber.KING),
                    Card(Genre.CLUB, CardNumber.ACE),
                    Card(Genre.CLUB, CardNumber.NINE),
                    # hand
                    Card(Genre.SPADE, CardNumber.FIVE),
                    Card(Genre.SPADE, CardNumber.SIX),
                ],
                [
                    Card(Genre.CLUB, CardNumber.THREE),
                    Card(Genre.HEART, CardNumber.THREE),
                    Card(Genre.DIAMOND, CardNumber.KING),
                    Card(Genre.CLUB, CardNumber.ACE),
                    Card(Genre.CLUB, CardNumber.NINE),
                    # hand
                    Card(Genre.DIAMOND, CardNumber.EIGHT),
                    Card(Genre.DIAMOND, CardNumber.TWO),
                ],
            ),
            (
                ">",
                [
                    Card(Genre.CLUB, CardNumber.THREE),
                    Card(Genre.HEART, CardNumber.THREE),
                    Card(Genre.DIAMOND, CardNumber.KING),
                    Card(Genre.CLUB, CardNumber.ACE),
                    Card(Genre.CLUB, CardNumber.NINE),
                    # hand
                    Card(Genre.CLUB, CardNumber.FIVE),
                    Card(Genre.CLUB, CardNumber.SIX),
                ],
                [
                    Card(Genre.CLUB, CardNumber.THREE),
                    Card(Genre.HEART, CardNumber.THREE),
                    Card(Genre.DIAMOND, CardNumber.KING),
                    Card(Genre.CLUB, CardNumber.ACE),
                    Card(Genre.CLUB, CardNumber.NINE),
                    # hand
                    Card(Genre.DIAMOND, CardNumber.EIGHT),
                    Card(Genre.DIAMOND, CardNumber.TWO),
                ],
            ),
        )

    @data_provider(_provide_7_card_hands_for_comparison)
    def test_comparison(self, op: str, first_hand, second_hand):
        # When
        e1 = EvaluatorOf7Cards(first_hand)
        e2 = EvaluatorOf7Cards(second_hand)

        # Then
        if op == "<":
            self.assertTrue(e1 < e2)
        elif op == "=":
            self.assertTrue(e1 == e2)
        else:
            self.assertTrue(e1 > e2)

    @data_provider(
        lambda: (
            (
                [
                    Card(Genre.DIAMOND, CardNumber.QUEEN),
                    Card(Genre.SPADE, CardNumber.QUEEN),
                    Card(Genre.SPADE, CardNumber.TWO),
                    Card(Genre.CLUB, CardNumber.JACK),
                    Card(Genre.SPADE, CardNumber.TEN),
                    Card(Genre.HEART, CardNumber.ACE),
                    Card(Genre.CLUB, CardNumber.SIX),
                ],
                [
                    Card(Genre.DIAMOND, CardNumber.QUEEN),
                    Card(Genre.HEART, CardNumber.QUEEN),
                    Card(Genre.SPADE, CardNumber.EIGHT),
                    Card(Genre.CLUB, CardNumber.JACK),
                    Card(Genre.HEART, CardNumber.TEN),
                    Card(Genre.HEART, CardNumber.ACE),
                    Card(Genre.CLUB, CardNumber.FIVE),
                ],
                True,  # QQAJT
            ),
            (
                [
                    Card(Genre.DIAMOND, CardNumber.QUEEN),
                    Card(Genre.HEART, CardNumber.QUEEN),
                    Card(Genre.CLUB, CardNumber.QUEEN),
                    Card(Genre.HEART, CardNumber.JACK),
                    Card(Genre.CLUB, CardNumber.JACK),
                    Card(Genre.HEART, CardNumber.ACE),
                    Card(Genre.CLUB, CardNumber.SIX),
                ],
                [
                    Card(Genre.DIAMOND, CardNumber.QUEEN),
                    Card(Genre.HEART, CardNumber.QUEEN),
                    Card(Genre.SPADE, CardNumber.QUEEN),
                    Card(Genre.SPADE, CardNumber.JACK),
                    Card(Genre.CLUB, CardNumber.JACK),
                    Card(Genre.CLUB, CardNumber.THREE),
                    Card(Genre.SPADE, CardNumber.TWO),
                ],
                True,  # QQQJJ
            ),
            (
                [
                    Card(Genre.DIAMOND, CardNumber.QUEEN),
                    Card(Genre.HEART, CardNumber.QUEEN),
                    Card(Genre.SPADE, CardNumber.TWO),
                    Card(Genre.CLUB, CardNumber.JACK),
                    Card(Genre.HEART, CardNumber.JACK),
                    Card(Genre.HEART, CardNumber.ACE),
                    Card(Genre.CLUB, CardNumber.SIX),
                ],
                [
                    Card(Genre.DIAMOND, CardNumber.QUEEN),
                    Card(Genre.HEART, CardNumber.QUEEN),
                    Card(Genre.SPADE, CardNumber.THREE),
                    Card(Genre.CLUB, CardNumber.JACK),
                    Card(Genre.HEART, CardNumber.ACE),
                    Card(Genre.CLUB, CardNumber.SIX),
                    Card(Genre.HEART, CardNumber.SIX),
                ],
                False,  # QQJJA != QQ66A
            ),
        )
    )
    def test_hashes(self, hand_1: List[Card], hand_2: List[Card], are_equal: bool) -> None:
        e1 = EvaluatorOf7Cards(hand_1)
        e2 = EvaluatorOf7Cards(hand_2)

        self.assertEqual(e1.__hash__() == e2.__hash__(), are_equal)
