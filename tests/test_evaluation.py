import unittest

from cards.Card import Card, CardNumber, Genre
from cards.Evaluator import Evaluator


class TestEvaluation(unittest.TestCase):
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
            Card(Genre.DIAMOND, CardNumber.NINE),
            Card(Genre.DIAMOND, CardNumber.ACE),
        ]
        self.assertFalse(Evaluator.is_flush(stack))

        # Five of a genre
        stack = [
            Card(Genre.DIAMOND, CardNumber.QUEEN),
            Card(Genre.DIAMOND, CardNumber.JACK),
            Card(Genre.DIAMOND, CardNumber.KING),
            Card(Genre.HEART, CardNumber.EIGHT),
            Card(Genre.CLUB, CardNumber.JACK),
            Card(Genre.DIAMOND, CardNumber.NINE),
            Card(Genre.DIAMOND, CardNumber.ACE),
        ]
        self.assertTrue(Evaluator.is_flush(stack))

        # More than 5 of a genre
        stack = [
            Card(Genre.CLUB, CardNumber.QUEEN),
            Card(Genre.CLUB, CardNumber.JACK),
            Card(Genre.CLUB, CardNumber.KING),
            Card(Genre.CLUB, CardNumber.EIGHT),
            Card(Genre.CLUB, CardNumber.JACK),
            Card(Genre.CLUB, CardNumber.NINE),
            Card(Genre.CLUB, CardNumber.ACE),
        ]
        self.assertTrue(Evaluator.is_flush(stack))

    def test_is_straight(self):
        # 2, 3, 4, 5, 6
        stack = [
            Card(Genre.CLUB, CardNumber.TWO),
            Card(Genre.CLUB, CardNumber.THREE),
            Card(Genre.HEART, CardNumber.FOUR),
            Card(Genre.CLUB, CardNumber.FIVE),
            Card(Genre.SPADE, CardNumber.SIX),
            Card(Genre.CLUB, CardNumber.NINE),
            Card(Genre.CLUB, CardNumber.ACE),
        ]
        self.assertTrue(Evaluator.is_straight(stack))

        # 10, J, Q, K, A
        stack = [
            Card(Genre.CLUB, CardNumber.TEN),
            Card(Genre.CLUB, CardNumber.KING),
            Card(Genre.CLUB, CardNumber.JACK),
            Card(Genre.HEART, CardNumber.QUEEN),
            Card(Genre.SPADE, CardNumber.SIX),
            Card(Genre.CLUB, CardNumber.NINE),
            Card(Genre.CLUB, CardNumber.ACE),
        ]
        self.assertTrue(Evaluator.is_straight(stack))

        # 1, 2, 3, 4, 5
        stack = [
            Card(Genre.CLUB, CardNumber.TWO),
            Card(Genre.CLUB, CardNumber.THREE),
            Card(Genre.HEART, CardNumber.FOUR),
            Card(Genre.CLUB, CardNumber.FIVE),
            Card(Genre.SPADE, CardNumber.KING),
            Card(Genre.CLUB, CardNumber.NINE),
            Card(Genre.CLUB, CardNumber.ACE),
        ]
        self.assertTrue(Evaluator.is_straight(stack))

        # Less than 5 distinct numbers
        stack = [
            Card(Genre.CLUB, CardNumber.TWO),
            Card(Genre.CLUB, CardNumber.THREE),
            Card(Genre.HEART, CardNumber.THREE),
            Card(Genre.CLUB, CardNumber.KING),
            Card(Genre.SPADE, CardNumber.KING),
            Card(Genre.HEART, CardNumber.KING),
            Card(Genre.CLUB, CardNumber.ACE),
        ]
        self.assertFalse(Evaluator.is_straight(stack))

        # J, Q, K, A, 2 is not a straight
        stack = [
            Card(Genre.CLUB, CardNumber.JACK),
            Card(Genre.HEART, CardNumber.QUEEN),
            Card(Genre.CLUB, CardNumber.KING),
            Card(Genre.SPADE, CardNumber.TWO),
            Card(Genre.CLUB, CardNumber.NINE),
            Card(Genre.DIAMOND, CardNumber.NINE),
            Card(Genre.CLUB, CardNumber.ACE),
        ]
        self.assertFalse(Evaluator.is_straight(stack))

        # No straight
        stack = [
            Card(Genre.CLUB, CardNumber.THREE),
            Card(Genre.HEART, CardNumber.FOUR),
            Card(Genre.CLUB, CardNumber.FIVE),
            Card(Genre.SPADE, CardNumber.SIX),
            Card(Genre.CLUB, CardNumber.NINE),
            Card(Genre.DIAMOND, CardNumber.NINE),
            Card(Genre.CLUB, CardNumber.ACE),
        ]
        self.assertFalse(Evaluator.is_straight(stack))

    def test_is_four_of_kind(self):
        stack = [
            Card(Genre.CLUB, CardNumber.THREE),
            Card(Genre.HEART, CardNumber.THREE),
            Card(Genre.DIAMOND, CardNumber.THREE),
            Card(Genre.SPADE, CardNumber.THREE),
            Card(Genre.CLUB, CardNumber.NINE),
            Card(Genre.DIAMOND, CardNumber.NINE),
            Card(Genre.CLUB, CardNumber.ACE),
        ]
        self.assertTrue(Evaluator.is_four_of_kind(stack))

        stack = [
            Card(Genre.CLUB, CardNumber.THREE),
            Card(Genre.HEART, CardNumber.KING),
            Card(Genre.DIAMOND, CardNumber.THREE),
            Card(Genre.SPADE, CardNumber.THREE),
            Card(Genre.CLUB, CardNumber.NINE),
            Card(Genre.DIAMOND, CardNumber.NINE),
            Card(Genre.CLUB, CardNumber.ACE),
        ]
        self.assertFalse(Evaluator.is_four_of_kind(stack))
