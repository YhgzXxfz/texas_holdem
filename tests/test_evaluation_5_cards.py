import unittest

from cards.Card import Card, CardNumber, Genre
from evaluations.Evaluation import Evaluation
from evaluations.EvaluatorOf5Cards import EvaluatorOf5Cards


class TestEvaluationOf5Cards(unittest.TestCase):
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

    def test_is_three_of_a_kind(self):
        stack = [
            Card(Genre.DIAMOND, CardNumber.QUEEN),
            Card(Genre.SPADE, CardNumber.QUEEN),
            Card(Genre.CLUB, CardNumber.QUEEN),
            Card(Genre.HEART, CardNumber.QUEEN),
            Card(Genre.CLUB, CardNumber.JACK),
        ]
        e = EvaluatorOf5Cards(stack)
        self.assertFalse(e.is_three_of_a_kind())

        stack = [
            Card(Genre.DIAMOND, CardNumber.QUEEN),
            Card(Genre.SPADE, CardNumber.QUEEN),
            Card(Genre.CLUB, CardNumber.QUEEN),
            Card(Genre.HEART, CardNumber.JACK),
            Card(Genre.CLUB, CardNumber.JACK),
        ]
        e = EvaluatorOf5Cards(stack)
        self.assertFalse(e.is_three_of_a_kind())

        stack = [
            Card(Genre.DIAMOND, CardNumber.QUEEN),
            Card(Genre.SPADE, CardNumber.QUEEN),
            Card(Genre.CLUB, CardNumber.QUEEN),
            Card(Genre.HEART, CardNumber.JACK),
            Card(Genre.CLUB, CardNumber.TEN),
        ]
        e = EvaluatorOf5Cards(stack)
        self.assertTrue(e.is_three_of_a_kind())

        stack = [
            Card(Genre.DIAMOND, CardNumber.QUEEN),
            Card(Genre.SPADE, CardNumber.QUEEN),
            Card(Genre.CLUB, CardNumber.JACK),
            Card(Genre.HEART, CardNumber.JACK),
            Card(Genre.CLUB, CardNumber.TEN),
        ]
        e = EvaluatorOf5Cards(stack)
        self.assertFalse(e.is_three_of_a_kind())

    def test_is_two_pairs(self):
        stack = [
            Card(Genre.DIAMOND, CardNumber.QUEEN),
            Card(Genre.SPADE, CardNumber.QUEEN),
            Card(Genre.CLUB, CardNumber.QUEEN),
            Card(Genre.HEART, CardNumber.QUEEN),
            Card(Genre.CLUB, CardNumber.JACK),
        ]
        e = EvaluatorOf5Cards(stack)
        self.assertFalse(e.is_two_pairs())

        stack = [
            Card(Genre.DIAMOND, CardNumber.QUEEN),
            Card(Genre.SPADE, CardNumber.QUEEN),
            Card(Genre.CLUB, CardNumber.QUEEN),
            Card(Genre.HEART, CardNumber.JACK),
            Card(Genre.CLUB, CardNumber.JACK),
        ]
        e = EvaluatorOf5Cards(stack)
        self.assertFalse(e.is_two_pairs())

        stack = [
            Card(Genre.DIAMOND, CardNumber.QUEEN),
            Card(Genre.SPADE, CardNumber.QUEEN),
            Card(Genre.CLUB, CardNumber.QUEEN),
            Card(Genre.HEART, CardNumber.JACK),
            Card(Genre.CLUB, CardNumber.TEN),
        ]
        e = EvaluatorOf5Cards(stack)
        self.assertFalse(e.is_two_pairs())

        stack = [
            Card(Genre.DIAMOND, CardNumber.QUEEN),
            Card(Genre.SPADE, CardNumber.QUEEN),
            Card(Genre.CLUB, CardNumber.JACK),
            Card(Genre.HEART, CardNumber.JACK),
            Card(Genre.CLUB, CardNumber.TEN),
        ]
        e = EvaluatorOf5Cards(stack)
        self.assertTrue(e.is_two_pairs())

    def test_is_one_pair(self):
        stack = [
            Card(Genre.DIAMOND, CardNumber.QUEEN),
            Card(Genre.SPADE, CardNumber.QUEEN),
            Card(Genre.CLUB, CardNumber.QUEEN),
            Card(Genre.HEART, CardNumber.QUEEN),
            Card(Genre.CLUB, CardNumber.JACK),
        ]
        e = EvaluatorOf5Cards(stack)
        self.assertFalse(e.is_one_pair())

        stack = [
            Card(Genre.DIAMOND, CardNumber.QUEEN),
            Card(Genre.SPADE, CardNumber.QUEEN),
            Card(Genre.CLUB, CardNumber.QUEEN),
            Card(Genre.HEART, CardNumber.JACK),
            Card(Genre.CLUB, CardNumber.JACK),
        ]
        e = EvaluatorOf5Cards(stack)
        self.assertFalse(e.is_one_pair())

        stack = [
            Card(Genre.DIAMOND, CardNumber.QUEEN),
            Card(Genre.SPADE, CardNumber.QUEEN),
            Card(Genre.CLUB, CardNumber.QUEEN),
            Card(Genre.HEART, CardNumber.JACK),
            Card(Genre.CLUB, CardNumber.TEN),
        ]
        e = EvaluatorOf5Cards(stack)
        self.assertFalse(e.is_one_pair())

        stack = [
            Card(Genre.DIAMOND, CardNumber.QUEEN),
            Card(Genre.SPADE, CardNumber.QUEEN),
            Card(Genre.CLUB, CardNumber.JACK),
            Card(Genre.HEART, CardNumber.JACK),
            Card(Genre.CLUB, CardNumber.TEN),
        ]
        e = EvaluatorOf5Cards(stack)
        self.assertFalse(e.is_one_pair())

        stack = [
            Card(Genre.DIAMOND, CardNumber.QUEEN),
            Card(Genre.SPADE, CardNumber.QUEEN),
            Card(Genre.CLUB, CardNumber.JACK),
            Card(Genre.HEART, CardNumber.ACE),
            Card(Genre.CLUB, CardNumber.TEN),
        ]
        e = EvaluatorOf5Cards(stack)
        self.assertTrue(e.is_one_pair())

    def test_evaluation(self):
        stack = [
            Card(Genre.DIAMOND, CardNumber.QUEEN),
            Card(Genre.DIAMOND, CardNumber.ACE),
            Card(Genre.DIAMOND, CardNumber.KING),
            Card(Genre.DIAMOND, CardNumber.TEN),
            Card(Genre.DIAMOND, CardNumber.JACK),
        ]
        e = EvaluatorOf5Cards(stack)
        self.assertEqual(e.getOptimalCards(), Evaluation.ROYAL_STRAIGHT_FLUSH)

        stack = [
            Card(Genre.DIAMOND, CardNumber.QUEEN),
            Card(Genre.DIAMOND, CardNumber.NINE),
            Card(Genre.DIAMOND, CardNumber.KING),
            Card(Genre.DIAMOND, CardNumber.TEN),
            Card(Genre.DIAMOND, CardNumber.JACK),
        ]
        e = EvaluatorOf5Cards(stack)
        self.assertEqual(e.getOptimalCards(), Evaluation.STRAIGHT_FLUSH)

        stack = [
            Card(Genre.DIAMOND, CardNumber.QUEEN),
            Card(Genre.SPADE, CardNumber.QUEEN),
            Card(Genre.CLUB, CardNumber.QUEEN),
            Card(Genre.HEART, CardNumber.QUEEN),
            Card(Genre.CLUB, CardNumber.JACK),
        ]
        e = EvaluatorOf5Cards(stack)
        self.assertEqual(e.getOptimalCards(), Evaluation.FOUR_OF_A_KIND)

        stack = [
            Card(Genre.DIAMOND, CardNumber.QUEEN),
            Card(Genre.SPADE, CardNumber.QUEEN),
            Card(Genre.CLUB, CardNumber.QUEEN),
            Card(Genre.HEART, CardNumber.JACK),
            Card(Genre.CLUB, CardNumber.JACK),
        ]
        e = EvaluatorOf5Cards(stack)
        self.assertEqual(e.getOptimalCards(), Evaluation.FULL_HOUSE)

        stack = [
            Card(Genre.DIAMOND, CardNumber.QUEEN),
            Card(Genre.DIAMOND, CardNumber.ACE),
            Card(Genre.DIAMOND, CardNumber.KING),
            Card(Genre.DIAMOND, CardNumber.EIGHT),
            Card(Genre.DIAMOND, CardNumber.JACK),
        ]
        e = EvaluatorOf5Cards(stack)
        self.assertEqual(e.getOptimalCards(), Evaluation.FLUSH)

        stack = [
            Card(Genre.DIAMOND, CardNumber.TWO),
            Card(Genre.SPADE, CardNumber.ACE),
            Card(Genre.SPADE, CardNumber.THREE),
            Card(Genre.HEART, CardNumber.FOUR),
            Card(Genre.CLUB, CardNumber.FIVE),
        ]
        e = EvaluatorOf5Cards(stack)
        self.assertEqual(e.getOptimalCards(), Evaluation.STRAIGHT)

        stack = [
            Card(Genre.DIAMOND, CardNumber.QUEEN),
            Card(Genre.SPADE, CardNumber.QUEEN),
            Card(Genre.CLUB, CardNumber.QUEEN),
            Card(Genre.HEART, CardNumber.JACK),
            Card(Genre.CLUB, CardNumber.TEN),
        ]
        e = EvaluatorOf5Cards(stack)
        self.assertEqual(e.getOptimalCards(), Evaluation.THREE_OF_A_KIND)

        stack = [
            Card(Genre.DIAMOND, CardNumber.QUEEN),
            Card(Genre.SPADE, CardNumber.QUEEN),
            Card(Genre.CLUB, CardNumber.JACK),
            Card(Genre.HEART, CardNumber.JACK),
            Card(Genre.CLUB, CardNumber.TEN),
        ]
        e = EvaluatorOf5Cards(stack)
        self.assertEqual(e.getOptimalCards(), Evaluation.TWO_PAIRS)

        stack = [
            Card(Genre.DIAMOND, CardNumber.QUEEN),
            Card(Genre.SPADE, CardNumber.QUEEN),
            Card(Genre.CLUB, CardNumber.JACK),
            Card(Genre.HEART, CardNumber.ACE),
            Card(Genre.CLUB, CardNumber.TEN),
        ]
        e = EvaluatorOf5Cards(stack)
        self.assertEqual(e.getOptimalCards(), Evaluation.ONE_PAIR)

        stack = [
            Card(Genre.DIAMOND, CardNumber.QUEEN),
            Card(Genre.SPADE, CardNumber.TWO),
            Card(Genre.CLUB, CardNumber.JACK),
            Card(Genre.HEART, CardNumber.ACE),
            Card(Genre.CLUB, CardNumber.TEN),
        ]
        e = EvaluatorOf5Cards(stack)
        self.assertEqual(e.getOptimalCards(), Evaluation.HIGH_CARD)

    def test_comparison_when_evalutations_are_different(self):
        stack = [
            Card(Genre.DIAMOND, CardNumber.QUEEN),
            Card(Genre.DIAMOND, CardNumber.ACE),
            Card(Genre.DIAMOND, CardNumber.KING),
            Card(Genre.DIAMOND, CardNumber.TEN),
            Card(Genre.DIAMOND, CardNumber.JACK),
        ]
        royal_straight_flush = EvaluatorOf5Cards(stack)

        stack = [
            Card(Genre.DIAMOND, CardNumber.QUEEN),
            Card(Genre.DIAMOND, CardNumber.NINE),
            Card(Genre.DIAMOND, CardNumber.KING),
            Card(Genre.DIAMOND, CardNumber.TEN),
            Card(Genre.DIAMOND, CardNumber.JACK),
        ]
        straight_flush = EvaluatorOf5Cards(stack)

        stack = [
            Card(Genre.DIAMOND, CardNumber.QUEEN),
            Card(Genre.SPADE, CardNumber.QUEEN),
            Card(Genre.CLUB, CardNumber.QUEEN),
            Card(Genre.HEART, CardNumber.QUEEN),
            Card(Genre.CLUB, CardNumber.JACK),
        ]
        four_of_a_kind = EvaluatorOf5Cards(stack)

        stack = [
            Card(Genre.DIAMOND, CardNumber.QUEEN),
            Card(Genre.SPADE, CardNumber.QUEEN),
            Card(Genre.CLUB, CardNumber.QUEEN),
            Card(Genre.HEART, CardNumber.JACK),
            Card(Genre.CLUB, CardNumber.JACK),
        ]
        full_house = EvaluatorOf5Cards(stack)

        stack = [
            Card(Genre.DIAMOND, CardNumber.QUEEN),
            Card(Genre.DIAMOND, CardNumber.ACE),
            Card(Genre.DIAMOND, CardNumber.KING),
            Card(Genre.DIAMOND, CardNumber.EIGHT),
            Card(Genre.DIAMOND, CardNumber.JACK),
        ]
        flush = EvaluatorOf5Cards(stack)

        stack = [
            Card(Genre.DIAMOND, CardNumber.TWO),
            Card(Genre.SPADE, CardNumber.ACE),
            Card(Genre.SPADE, CardNumber.THREE),
            Card(Genre.HEART, CardNumber.FOUR),
            Card(Genre.CLUB, CardNumber.FIVE),
        ]
        straight = EvaluatorOf5Cards(stack)

        stack = [
            Card(Genre.DIAMOND, CardNumber.QUEEN),
            Card(Genre.SPADE, CardNumber.QUEEN),
            Card(Genre.CLUB, CardNumber.QUEEN),
            Card(Genre.HEART, CardNumber.JACK),
            Card(Genre.CLUB, CardNumber.TEN),
        ]
        three_of_a_kind = EvaluatorOf5Cards(stack)

        stack = [
            Card(Genre.DIAMOND, CardNumber.QUEEN),
            Card(Genre.SPADE, CardNumber.QUEEN),
            Card(Genre.CLUB, CardNumber.JACK),
            Card(Genre.HEART, CardNumber.JACK),
            Card(Genre.CLUB, CardNumber.TEN),
        ]
        two_pairs = EvaluatorOf5Cards(stack)

        stack = [
            Card(Genre.DIAMOND, CardNumber.QUEEN),
            Card(Genre.SPADE, CardNumber.QUEEN),
            Card(Genre.CLUB, CardNumber.JACK),
            Card(Genre.HEART, CardNumber.ACE),
            Card(Genre.CLUB, CardNumber.TEN),
        ]
        one_pair = EvaluatorOf5Cards(stack)

        stack = [
            Card(Genre.DIAMOND, CardNumber.QUEEN),
            Card(Genre.SPADE, CardNumber.TWO),
            Card(Genre.CLUB, CardNumber.JACK),
            Card(Genre.HEART, CardNumber.ACE),
            Card(Genre.CLUB, CardNumber.TEN),
        ]
        high_card = EvaluatorOf5Cards(stack)

        self.assertLess(high_card, one_pair)
        self.assertLess(one_pair, two_pairs)
        self.assertLess(two_pairs, three_of_a_kind)
        self.assertLess(three_of_a_kind, straight)
        self.assertLess(straight, flush)
        self.assertLess(flush, full_house)
        self.assertLess(full_house, four_of_a_kind)
        self.assertLess(four_of_a_kind, straight_flush)
        self.assertLess(straight_flush, royal_straight_flush)

    def test_comparisons_when_evaluations_are_high_cards(self):
        stack = [
            Card(Genre.DIAMOND, CardNumber.QUEEN),
            Card(Genre.SPADE, CardNumber.TWO),
            Card(Genre.CLUB, CardNumber.JACK),
            Card(Genre.HEART, CardNumber.ACE),
            Card(Genre.CLUB, CardNumber.SIX),
        ]
        high_card_AQJ62 = EvaluatorOf5Cards(stack)

        stack = [
            Card(Genre.DIAMOND, CardNumber.QUEEN),
            Card(Genre.SPADE, CardNumber.TWO),
            Card(Genre.DIAMOND, CardNumber.NINE),
            Card(Genre.HEART, CardNumber.ACE),
            Card(Genre.CLUB, CardNumber.TEN),
        ]
        high_card_AQT92 = EvaluatorOf5Cards(stack)
        self.assertEqual(high_card_AQJ62.getOptimalCards(), Evaluation.HIGH_CARD)
        self.assertEqual(high_card_AQT92.getOptimalCards(), Evaluation.HIGH_CARD)
        self.assertLess(high_card_AQT92, high_card_AQJ62)

    def test_comparisons_when_evaluations_are_one_pair(self):
        # pair dominates
        stack = [
            Card(Genre.DIAMOND, CardNumber.QUEEN),
            Card(Genre.SPADE, CardNumber.TWO),
            Card(Genre.SPADE, CardNumber.JACK),
            Card(Genre.HEART, CardNumber.ACE),
            Card(Genre.CLUB, CardNumber.JACK),
        ]
        one_pair_JJAQ2 = EvaluatorOf5Cards(stack)

        stack = [
            Card(Genre.HEART, CardNumber.QUEEN),
            Card(Genre.SPADE, CardNumber.TWO),
            Card(Genre.DIAMOND, CardNumber.QUEEN),
            Card(Genre.HEART, CardNumber.ACE),
            Card(Genre.CLUB, CardNumber.TEN),
        ]
        one_pair_QQAT2 = EvaluatorOf5Cards(stack)
        self.assertEqual(one_pair_JJAQ2.getOptimalCards(), Evaluation.ONE_PAIR)
        self.assertEqual(one_pair_QQAT2.getOptimalCards(), Evaluation.ONE_PAIR)
        self.assertLess(one_pair_JJAQ2, one_pair_QQAT2)

        # pairs are equal, high card dominates
        stack = [
            Card(Genre.DIAMOND, CardNumber.QUEEN),
            Card(Genre.SPADE, CardNumber.TWO),
            Card(Genre.SPADE, CardNumber.JACK),
            Card(Genre.HEART, CardNumber.ACE),
            Card(Genre.CLUB, CardNumber.JACK),
        ]
        one_pair_JJAQ2 = EvaluatorOf5Cards(stack)

        stack = [
            Card(Genre.HEART, CardNumber.JACK),
            Card(Genre.SPADE, CardNumber.TWO),
            Card(Genre.DIAMOND, CardNumber.JACK),
            Card(Genre.HEART, CardNumber.ACE),
            Card(Genre.CLUB, CardNumber.TEN),
        ]
        one_pair_JJAT2 = EvaluatorOf5Cards(stack)
        self.assertEqual(one_pair_JJAQ2.getOptimalCards(), Evaluation.ONE_PAIR)
        self.assertEqual(one_pair_JJAT2.getOptimalCards(), Evaluation.ONE_PAIR)
        self.assertLess(one_pair_JJAT2, one_pair_JJAQ2)

    def test_comparisons_when_evaluations_are_two_pairs(self):
        # bigger pair dominates
        stack = [
            Card(Genre.DIAMOND, CardNumber.QUEEN),
            Card(Genre.SPADE, CardNumber.ACE),
            Card(Genre.SPADE, CardNumber.JACK),
            Card(Genre.HEART, CardNumber.QUEEN),
            Card(Genre.CLUB, CardNumber.JACK),
        ]
        two_pairs_QQJJA = EvaluatorOf5Cards(stack)

        stack = [
            Card(Genre.HEART, CardNumber.QUEEN),
            Card(Genre.SPADE, CardNumber.TWO),
            Card(Genre.DIAMOND, CardNumber.ACE),
            Card(Genre.HEART, CardNumber.ACE),
            Card(Genre.CLUB, CardNumber.TWO),
        ]
        two_pairs_AA22Q = EvaluatorOf5Cards(stack)
        self.assertEqual(two_pairs_QQJJA.getOptimalCards(), Evaluation.TWO_PAIRS)
        self.assertEqual(two_pairs_AA22Q.getOptimalCards(), Evaluation.TWO_PAIRS)
        self.assertLess(two_pairs_QQJJA, two_pairs_AA22Q)

        # bigger pairs are equal, second pair dominates
        stack = [
            Card(Genre.DIAMOND, CardNumber.TEN),
            Card(Genre.SPADE, CardNumber.KING),
            Card(Genre.SPADE, CardNumber.JACK),
            Card(Genre.HEART, CardNumber.TEN),
            Card(Genre.CLUB, CardNumber.JACK),
        ]
        two_pairs_JJTTK = EvaluatorOf5Cards(stack)

        stack = [
            Card(Genre.HEART, CardNumber.JACK),
            Card(Genre.SPADE, CardNumber.SIX),
            Card(Genre.DIAMOND, CardNumber.JACK),
            Card(Genre.HEART, CardNumber.ACE),
            Card(Genre.CLUB, CardNumber.SIX),
        ]
        two_pairs_JJ66A = EvaluatorOf5Cards(stack)
        self.assertEqual(two_pairs_JJTTK.getOptimalCards(), Evaluation.TWO_PAIRS)
        self.assertEqual(two_pairs_JJ66A.getOptimalCards(), Evaluation.TWO_PAIRS)
        self.assertLess(two_pairs_JJ66A, two_pairs_JJTTK)

        # pairs are equal, high card dominates
        stack = [
            Card(Genre.DIAMOND, CardNumber.TEN),
            Card(Genre.SPADE, CardNumber.KING),
            Card(Genre.SPADE, CardNumber.JACK),
            Card(Genre.HEART, CardNumber.TEN),
            Card(Genre.CLUB, CardNumber.JACK),
        ]
        two_pairs_JJTTK = EvaluatorOf5Cards(stack)

        stack = [
            Card(Genre.HEART, CardNumber.JACK),
            Card(Genre.SPADE, CardNumber.TEN),
            Card(Genre.DIAMOND, CardNumber.JACK),
            Card(Genre.HEART, CardNumber.ACE),
            Card(Genre.CLUB, CardNumber.TEN),
        ]
        two_pairs_JJTTA = EvaluatorOf5Cards(stack)
        self.assertEqual(two_pairs_JJTTK.getOptimalCards(), Evaluation.TWO_PAIRS)
        self.assertEqual(two_pairs_JJTTA.getOptimalCards(), Evaluation.TWO_PAIRS)
        self.assertLess(two_pairs_JJTTK, two_pairs_JJTTA)

    def test_comparisons_when_evaluations_are_three_of_a_kind(self):
        # tripes dominate
        stack = [
            Card(Genre.DIAMOND, CardNumber.QUEEN),
            Card(Genre.SPADE, CardNumber.QUEEN),
            Card(Genre.SPADE, CardNumber.SIX),
            Card(Genre.HEART, CardNumber.QUEEN),
            Card(Genre.CLUB, CardNumber.JACK),
        ]
        tripes_QQQJ6 = EvaluatorOf5Cards(stack)

        stack = [
            Card(Genre.DIAMOND, CardNumber.KING),
            Card(Genre.SPADE, CardNumber.KING),
            Card(Genre.SPADE, CardNumber.SIX),
            Card(Genre.HEART, CardNumber.KING),
            Card(Genre.CLUB, CardNumber.JACK),
        ]
        tripes_KKKJ6 = EvaluatorOf5Cards(stack)
        self.assertEqual(tripes_QQQJ6.getOptimalCards(), Evaluation.THREE_OF_A_KIND)
        self.assertEqual(tripes_KKKJ6.getOptimalCards(), Evaluation.THREE_OF_A_KIND)
        self.assertLess(tripes_QQQJ6, tripes_KKKJ6)

        # tripes are equal, high card dominates
        stack = [
            Card(Genre.DIAMOND, CardNumber.QUEEN),
            Card(Genre.SPADE, CardNumber.QUEEN),
            Card(Genre.SPADE, CardNumber.SIX),
            Card(Genre.HEART, CardNumber.QUEEN),
            Card(Genre.CLUB, CardNumber.JACK),
        ]
        tripes_QQQJ6 = EvaluatorOf5Cards(stack)

        stack = [
            Card(Genre.DIAMOND, CardNumber.QUEEN),
            Card(Genre.SPADE, CardNumber.QUEEN),
            Card(Genre.SPADE, CardNumber.FIVE),
            Card(Genre.HEART, CardNumber.QUEEN),
            Card(Genre.CLUB, CardNumber.ACE),
        ]
        tripes_QQQA5 = EvaluatorOf5Cards(stack)
        self.assertEqual(tripes_QQQJ6.getOptimalCards(), Evaluation.THREE_OF_A_KIND)
        self.assertEqual(tripes_QQQA5.getOptimalCards(), Evaluation.THREE_OF_A_KIND)
        self.assertLess(tripes_QQQJ6, tripes_QQQA5)

    def test_comparisons_when_evaluations_are_full_houses(self):
        # tripes dominate
        stack = [
            Card(Genre.DIAMOND, CardNumber.QUEEN),
            Card(Genre.SPADE, CardNumber.QUEEN),
            Card(Genre.SPADE, CardNumber.JACK),
            Card(Genre.HEART, CardNumber.QUEEN),
            Card(Genre.CLUB, CardNumber.JACK),
        ]
        full_house_QQQJJ = EvaluatorOf5Cards(stack)

        stack = [
            Card(Genre.DIAMOND, CardNumber.TEN),
            Card(Genre.SPADE, CardNumber.TEN),
            Card(Genre.SPADE, CardNumber.ACE),
            Card(Genre.HEART, CardNumber.TEN),
            Card(Genre.CLUB, CardNumber.ACE),
        ]
        full_house_TTTAA = EvaluatorOf5Cards(stack)
        self.assertEqual(full_house_QQQJJ.getOptimalCards(), Evaluation.FULL_HOUSE)
        self.assertEqual(full_house_TTTAA.getOptimalCards(), Evaluation.FULL_HOUSE)
        self.assertLess(full_house_TTTAA, full_house_QQQJJ)

        # tripes are equal, pairs dominate
        stack = [
            Card(Genre.DIAMOND, CardNumber.TEN),
            Card(Genre.SPADE, CardNumber.TEN),
            Card(Genre.SPADE, CardNumber.ACE),
            Card(Genre.HEART, CardNumber.TEN),
            Card(Genre.CLUB, CardNumber.ACE),
        ]
        full_house_TTTAA = EvaluatorOf5Cards(stack)

        stack = [
            Card(Genre.DIAMOND, CardNumber.TEN),
            Card(Genre.SPADE, CardNumber.TEN),
            Card(Genre.SPADE, CardNumber.KING),
            Card(Genre.HEART, CardNumber.TEN),
            Card(Genre.CLUB, CardNumber.KING),
        ]
        full_house_TTTKK = EvaluatorOf5Cards(stack)
        self.assertEqual(full_house_TTTAA.getOptimalCards(), Evaluation.FULL_HOUSE)
        self.assertEqual(full_house_TTTKK.getOptimalCards(), Evaluation.FULL_HOUSE)
        self.assertLess(full_house_TTTKK, full_house_TTTAA)
