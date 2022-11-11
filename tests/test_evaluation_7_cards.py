import unittest

from cards.Card import Card, CardNumber, Genre
from evaluations.Evaluation import Evaluation
from evaluations.EvaluatorOf5Cards import EvaluatorOf5Cards
from evaluations.EvaluatorOf7Cards import EvaluatorOf7Cards
from unittest_data_provider import data_provider


class TestEvaluationOf7Cards(unittest.TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def provide_7_card_hands():
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
        )

    @data_provider(provide_7_card_hands)
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
