import unittest

from cards.Card import Card, CardNumber, Genre


class TestCardsAreDifferent(unittest.TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def test_no_redundants(self):
        stack = [
            Card(Genre.DIAMOND, CardNumber.TWO),
            Card(Genre.DIAMOND, CardNumber.THREE),
            Card(Genre.DIAMOND, CardNumber.FOUR),
            Card(Genre.DIAMOND, CardNumber.FIVE),
            Card(Genre.DIAMOND, CardNumber.SIX),
            Card(Genre.DIAMOND, CardNumber.SEVEN),
            Card(Genre.DIAMOND, CardNumber.EIGHT),
            Card(Genre.DIAMOND, CardNumber.NINE),
            Card(Genre.DIAMOND, CardNumber.TEN),
            Card(Genre.DIAMOND, CardNumber.JACK),
            Card(Genre.DIAMOND, CardNumber.QUEEN),
            Card(Genre.DIAMOND, CardNumber.KING),
            Card(Genre.DIAMOND, CardNumber.ACE),
            Card(Genre.HEART, CardNumber.TWO),
            Card(Genre.HEART, CardNumber.THREE),
            Card(Genre.HEART, CardNumber.FOUR),
            Card(Genre.HEART, CardNumber.FIVE),
            Card(Genre.HEART, CardNumber.SIX),
            Card(Genre.HEART, CardNumber.SEVEN),
            Card(Genre.HEART, CardNumber.EIGHT),
            Card(Genre.HEART, CardNumber.NINE),
            Card(Genre.HEART, CardNumber.TEN),
            Card(Genre.HEART, CardNumber.JACK),
            Card(Genre.HEART, CardNumber.QUEEN),
            Card(Genre.HEART, CardNumber.KING),
            Card(Genre.HEART, CardNumber.ACE),
            Card(Genre.CLUB, CardNumber.TWO),
            Card(Genre.CLUB, CardNumber.THREE),
            Card(Genre.CLUB, CardNumber.FOUR),
            Card(Genre.CLUB, CardNumber.FIVE),
            Card(Genre.CLUB, CardNumber.SIX),
            Card(Genre.CLUB, CardNumber.SEVEN),
            Card(Genre.CLUB, CardNumber.EIGHT),
            Card(Genre.CLUB, CardNumber.NINE),
            Card(Genre.CLUB, CardNumber.TEN),
            Card(Genre.CLUB, CardNumber.JACK),
            Card(Genre.CLUB, CardNumber.QUEEN),
            Card(Genre.CLUB, CardNumber.KING),
            Card(Genre.CLUB, CardNumber.ACE),
            Card(Genre.SPADE, CardNumber.TWO),
            Card(Genre.SPADE, CardNumber.THREE),
            Card(Genre.SPADE, CardNumber.FOUR),
            Card(Genre.SPADE, CardNumber.FIVE),
            Card(Genre.SPADE, CardNumber.SIX),
            Card(Genre.SPADE, CardNumber.SEVEN),
            Card(Genre.SPADE, CardNumber.EIGHT),
            Card(Genre.SPADE, CardNumber.NINE),
            Card(Genre.SPADE, CardNumber.TEN),
            Card(Genre.SPADE, CardNumber.JACK),
            Card(Genre.SPADE, CardNumber.QUEEN),
            Card(Genre.SPADE, CardNumber.KING),
            Card(Genre.SPADE, CardNumber.ACE),
        ]
        self.assertEqual(len(set(stack)), len(stack))
