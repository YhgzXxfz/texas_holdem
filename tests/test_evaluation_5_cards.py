import unittest

from cards.Card import Card, CardNumber, Genre
from cards.Evaluator import EvaluatorOf5Cards


class TestEvaluationOf7Cards(unittest.TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def test_is_flush(self):
        # Not a flush
        stack = [
            Card(Genre.DIAMOND, CardNumber.QUEEN),
            Card(Genre.SPADE, CardNumber.ACE),
            Card(Genre.SPADE, CardNumber.KING),
            Card(Genre.HEART, CardNumber.EIGHT),
            Card(Genre.CLUB, CardNumber.JACK),
        ]
        e = EvaluatorOf5Cards(stack)
        self.assertFalse(e.is_flush())

        stack = [
            Card(Genre.DIAMOND, CardNumber.QUEEN),
            Card(Genre.DIAMOND, CardNumber.ACE),
            Card(Genre.DIAMOND, CardNumber.KING),
            Card(Genre.DIAMOND, CardNumber.EIGHT),
            Card(Genre.DIAMOND, CardNumber.JACK),
        ]
        e = EvaluatorOf5Cards(stack)
        self.assertTrue(e.is_flush())

    def test_is_straight(self):
        # Not a straight
        stack = [
            Card(Genre.DIAMOND, CardNumber.QUEEN),
            Card(Genre.SPADE, CardNumber.ACE),
            Card(Genre.SPADE, CardNumber.KING),
            Card(Genre.HEART, CardNumber.EIGHT),
            Card(Genre.CLUB, CardNumber.JACK),
        ]
        e = EvaluatorOf5Cards(stack)
        self.assertFalse(e.is_straight())

        stack = [
            Card(Genre.DIAMOND, CardNumber.QUEEN),
            Card(Genre.SPADE, CardNumber.ACE),
            Card(Genre.SPADE, CardNumber.KING),
            Card(Genre.HEART, CardNumber.TEN),
            Card(Genre.CLUB, CardNumber.JACK),
        ]
        e = EvaluatorOf5Cards(stack)
        self.assertTrue(e.is_straight())

        stack = [
            Card(Genre.DIAMOND, CardNumber.TWO),
            Card(Genre.SPADE, CardNumber.ACE),
            Card(Genre.SPADE, CardNumber.THREE),
            Card(Genre.HEART, CardNumber.FOUR),
            Card(Genre.CLUB, CardNumber.FIVE),
        ]
        e = EvaluatorOf5Cards(stack)
        self.assertTrue(e.is_straight())
