import unittest

from cards.Card import Card, CardNumber, Genre
from evaluations.EvaluatorOf5Cards import EvaluatorOf5Cards
from evaluations.EvaluatorOf7Cards import EvaluatorOf7Cards


class TestEvaluationOf7Cards(unittest.TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def test_get_optimal_hands(self):
        # Given
        stack = [
            Card(Genre.CLUB, CardNumber.THREE),
            Card(Genre.HEART, CardNumber.THREE),
            Card(Genre.DIAMOND, CardNumber.THREE),
            Card(Genre.SPADE, CardNumber.THREE),
            Card(Genre.CLUB, CardNumber.NINE),
            Card(Genre.DIAMOND, CardNumber.NINE),
            Card(Genre.CLUB, CardNumber.ACE),
        ]

        # When
        e = EvaluatorOf7Cards(stack)
        best = e.getOptimalHands()

        # Then
        self.assertTrue(
            best
            == EvaluatorOf5Cards(
                [
                    Card(Genre.CLUB, CardNumber.THREE),
                    Card(Genre.HEART, CardNumber.THREE),
                    Card(Genre.DIAMOND, CardNumber.THREE),
                    Card(Genre.SPADE, CardNumber.THREE),
                    Card(Genre.CLUB, CardNumber.ACE),
                ]
            ),
            msg="Best hand is quads plus an Ace high card.",
        )
        self.assertTrue(set(best.original_cards) <= set(stack), msg="Best hand should be a subset of the 7 cards.")
