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

    def test_is_straight_flush(self):
        # staight but not flush
        stack = [
            Card(Genre.DIAMOND, CardNumber.QUEEN),
            Card(Genre.SPADE, CardNumber.ACE),
            Card(Genre.SPADE, CardNumber.KING),
            Card(Genre.HEART, CardNumber.TEN),
            Card(Genre.CLUB, CardNumber.JACK),
        ]
        e = EvaluatorOf5Cards(stack)
        self.assertFalse(e.is_straight_flush())

        # flush but not straight
        stack = [
            Card(Genre.DIAMOND, CardNumber.QUEEN),
            Card(Genre.DIAMOND, CardNumber.ACE),
            Card(Genre.DIAMOND, CardNumber.KING),
            Card(Genre.DIAMOND, CardNumber.NINE),
            Card(Genre.DIAMOND, CardNumber.JACK),
        ]
        e = EvaluatorOf5Cards(stack)
        self.assertFalse(e.is_straight_flush())

        # straight flush
        stack = [
            Card(Genre.DIAMOND, CardNumber.QUEEN),
            Card(Genre.DIAMOND, CardNumber.ACE),
            Card(Genre.DIAMOND, CardNumber.KING),
            Card(Genre.DIAMOND, CardNumber.TEN),
            Card(Genre.DIAMOND, CardNumber.JACK),
        ]
        e = EvaluatorOf5Cards(stack)
        self.assertTrue(e.is_straight_flush())

    def test_is_royal_straight_flush(self):
        # royal straight flush
        stack = [
            Card(Genre.DIAMOND, CardNumber.QUEEN),
            Card(Genre.DIAMOND, CardNumber.ACE),
            Card(Genre.DIAMOND, CardNumber.KING),
            Card(Genre.DIAMOND, CardNumber.TEN),
            Card(Genre.DIAMOND, CardNumber.JACK),
        ]
        e = EvaluatorOf5Cards(stack)
        self.assertTrue(e.is_royal_straight_flush())

        stack = [
            Card(Genre.DIAMOND, CardNumber.QUEEN),
            Card(Genre.DIAMOND, CardNumber.NINE),
            Card(Genre.DIAMOND, CardNumber.KING),
            Card(Genre.DIAMOND, CardNumber.TEN),
            Card(Genre.DIAMOND, CardNumber.JACK),
        ]
        e = EvaluatorOf5Cards(stack)
        self.assertFalse(e.is_royal_straight_flush())

        stack = [
            Card(Genre.DIAMOND, CardNumber.ACE),
            Card(Genre.DIAMOND, CardNumber.TWO),
            Card(Genre.DIAMOND, CardNumber.THREE),
            Card(Genre.DIAMOND, CardNumber.FOUR),
            Card(Genre.DIAMOND, CardNumber.FIVE),
        ]
        e = EvaluatorOf5Cards(stack)
        self.assertFalse(e.is_royal_straight_flush())

    def test_is_four_of_a_kind(self):
        stack = [
            Card(Genre.DIAMOND, CardNumber.QUEEN),
            Card(Genre.SPADE, CardNumber.QUEEN),
            Card(Genre.CLUB, CardNumber.QUEEN),
            Card(Genre.HEART, CardNumber.QUEEN),
            Card(Genre.CLUB, CardNumber.JACK),
        ]
        e = EvaluatorOf5Cards(stack)
        self.assertTrue(e.is_four_of_a_kind())

        stack = [
            Card(Genre.DIAMOND, CardNumber.QUEEN),
            Card(Genre.SPADE, CardNumber.QUEEN),
            Card(Genre.CLUB, CardNumber.QUEEN),
            Card(Genre.HEART, CardNumber.JACK),
            Card(Genre.CLUB, CardNumber.JACK),
        ]
        e = EvaluatorOf5Cards(stack)
        self.assertFalse(e.is_four_of_a_kind())

    def test_is_full_house(self):
        stack = [
            Card(Genre.DIAMOND, CardNumber.QUEEN),
            Card(Genre.SPADE, CardNumber.QUEEN),
            Card(Genre.CLUB, CardNumber.QUEEN),
            Card(Genre.HEART, CardNumber.QUEEN),
            Card(Genre.CLUB, CardNumber.JACK),
        ]
        e = EvaluatorOf5Cards(stack)
        self.assertFalse(e.is_full_house())

        stack = [
            Card(Genre.DIAMOND, CardNumber.QUEEN),
            Card(Genre.SPADE, CardNumber.QUEEN),
            Card(Genre.CLUB, CardNumber.QUEEN),
            Card(Genre.HEART, CardNumber.JACK),
            Card(Genre.CLUB, CardNumber.TEN),
        ]
        e = EvaluatorOf5Cards(stack)
        self.assertFalse(e.is_full_house())

        stack = [
            Card(Genre.DIAMOND, CardNumber.QUEEN),
            Card(Genre.SPADE, CardNumber.QUEEN),
            Card(Genre.CLUB, CardNumber.JACK),
            Card(Genre.HEART, CardNumber.JACK),
            Card(Genre.CLUB, CardNumber.TEN),
        ]
        e = EvaluatorOf5Cards(stack)
        self.assertFalse(e.is_full_house())

        stack = [
            Card(Genre.DIAMOND, CardNumber.QUEEN),
            Card(Genre.SPADE, CardNumber.QUEEN),
            Card(Genre.CLUB, CardNumber.QUEEN),
            Card(Genre.HEART, CardNumber.JACK),
            Card(Genre.CLUB, CardNumber.JACK),
        ]
        e = EvaluatorOf5Cards(stack)
        self.assertTrue(e.is_full_house())
