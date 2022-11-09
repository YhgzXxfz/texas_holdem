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
        self.assertEqual(e.getEvaluation(), Evaluation.ROYAL_STRAIGHT_FLUSH)

        stack = [
            Card(Genre.DIAMOND, CardNumber.QUEEN),
            Card(Genre.DIAMOND, CardNumber.NINE),
            Card(Genre.DIAMOND, CardNumber.KING),
            Card(Genre.DIAMOND, CardNumber.TEN),
            Card(Genre.DIAMOND, CardNumber.JACK),
        ]
        e = EvaluatorOf5Cards(stack)
        self.assertEqual(e.getEvaluation(), Evaluation.STRAIGHT_FLUSH)

        stack = [
            Card(Genre.DIAMOND, CardNumber.QUEEN),
            Card(Genre.SPADE, CardNumber.QUEEN),
            Card(Genre.CLUB, CardNumber.QUEEN),
            Card(Genre.HEART, CardNumber.QUEEN),
            Card(Genre.CLUB, CardNumber.JACK),
        ]
        e = EvaluatorOf5Cards(stack)
        self.assertEqual(e.getEvaluation(), Evaluation.FOUR_OF_A_KIND)

        stack = [
            Card(Genre.DIAMOND, CardNumber.QUEEN),
            Card(Genre.SPADE, CardNumber.QUEEN),
            Card(Genre.CLUB, CardNumber.QUEEN),
            Card(Genre.HEART, CardNumber.JACK),
            Card(Genre.CLUB, CardNumber.JACK),
        ]
        e = EvaluatorOf5Cards(stack)
        self.assertEqual(e.getEvaluation(), Evaluation.FULL_HOUSE)

        stack = [
            Card(Genre.DIAMOND, CardNumber.QUEEN),
            Card(Genre.DIAMOND, CardNumber.ACE),
            Card(Genre.DIAMOND, CardNumber.KING),
            Card(Genre.DIAMOND, CardNumber.EIGHT),
            Card(Genre.DIAMOND, CardNumber.JACK),
        ]
        e = EvaluatorOf5Cards(stack)
        self.assertEqual(e.getEvaluation(), Evaluation.FLUSH)

        stack = [
            Card(Genre.DIAMOND, CardNumber.TWO),
            Card(Genre.SPADE, CardNumber.ACE),
            Card(Genre.SPADE, CardNumber.THREE),
            Card(Genre.HEART, CardNumber.FOUR),
            Card(Genre.CLUB, CardNumber.FIVE),
        ]
        e = EvaluatorOf5Cards(stack)
        self.assertEqual(e.getEvaluation(), Evaluation.STRAIGHT)

        stack = [
            Card(Genre.DIAMOND, CardNumber.QUEEN),
            Card(Genre.SPADE, CardNumber.QUEEN),
            Card(Genre.CLUB, CardNumber.QUEEN),
            Card(Genre.HEART, CardNumber.JACK),
            Card(Genre.CLUB, CardNumber.TEN),
        ]
        e = EvaluatorOf5Cards(stack)
        self.assertEqual(e.getEvaluation(), Evaluation.THREE_OF_A_KIND)

        stack = [
            Card(Genre.DIAMOND, CardNumber.QUEEN),
            Card(Genre.SPADE, CardNumber.QUEEN),
            Card(Genre.CLUB, CardNumber.JACK),
            Card(Genre.HEART, CardNumber.JACK),
            Card(Genre.CLUB, CardNumber.TEN),
        ]
        e = EvaluatorOf5Cards(stack)
        self.assertEqual(e.getEvaluation(), Evaluation.TWO_PAIRS)

        stack = [
            Card(Genre.DIAMOND, CardNumber.QUEEN),
            Card(Genre.SPADE, CardNumber.QUEEN),
            Card(Genre.CLUB, CardNumber.JACK),
            Card(Genre.HEART, CardNumber.ACE),
            Card(Genre.CLUB, CardNumber.TEN),
        ]
        e = EvaluatorOf5Cards(stack)
        self.assertEqual(e.getEvaluation(), Evaluation.ONE_PAIR)

        stack = [
            Card(Genre.DIAMOND, CardNumber.QUEEN),
            Card(Genre.SPADE, CardNumber.TWO),
            Card(Genre.CLUB, CardNumber.JACK),
            Card(Genre.HEART, CardNumber.ACE),
            Card(Genre.CLUB, CardNumber.TEN),
        ]
        e = EvaluatorOf5Cards(stack)
        self.assertEqual(e.getEvaluation(), Evaluation.HIGH_CARD)

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
        self.assertEqual(high_card_AQJ62.getEvaluation(), Evaluation.HIGH_CARD)
        self.assertEqual(high_card_AQT92.getEvaluation(), Evaluation.HIGH_CARD)
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
        self.assertEqual(one_pair_JJAQ2.getEvaluation(), Evaluation.ONE_PAIR)
        self.assertEqual(one_pair_QQAT2.getEvaluation(), Evaluation.ONE_PAIR)
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
        self.assertEqual(one_pair_JJAQ2.getEvaluation(), Evaluation.ONE_PAIR)
        self.assertEqual(one_pair_JJAT2.getEvaluation(), Evaluation.ONE_PAIR)
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
        self.assertEqual(two_pairs_QQJJA.getEvaluation(), Evaluation.TWO_PAIRS)
        self.assertEqual(two_pairs_AA22Q.getEvaluation(), Evaluation.TWO_PAIRS)
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
        self.assertEqual(two_pairs_JJTTK.getEvaluation(), Evaluation.TWO_PAIRS)
        self.assertEqual(two_pairs_JJ66A.getEvaluation(), Evaluation.TWO_PAIRS)
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
        self.assertEqual(two_pairs_JJTTK.getEvaluation(), Evaluation.TWO_PAIRS)
        self.assertEqual(two_pairs_JJTTA.getEvaluation(), Evaluation.TWO_PAIRS)
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
        self.assertEqual(tripes_QQQJ6.getEvaluation(), Evaluation.THREE_OF_A_KIND)
        self.assertEqual(tripes_KKKJ6.getEvaluation(), Evaluation.THREE_OF_A_KIND)
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
        self.assertEqual(tripes_QQQJ6.getEvaluation(), Evaluation.THREE_OF_A_KIND)
        self.assertEqual(tripes_QQQA5.getEvaluation(), Evaluation.THREE_OF_A_KIND)
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
        self.assertEqual(full_house_QQQJJ.getEvaluation(), Evaluation.FULL_HOUSE)
        self.assertEqual(full_house_TTTAA.getEvaluation(), Evaluation.FULL_HOUSE)
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
        self.assertEqual(full_house_TTTAA.getEvaluation(), Evaluation.FULL_HOUSE)
        self.assertEqual(full_house_TTTKK.getEvaluation(), Evaluation.FULL_HOUSE)
        self.assertLess(full_house_TTTKK, full_house_TTTAA)

    def test_comparisons_when_evaluations_are_four_of_a_kind(self):
        # quads dominate
        stack = [
            Card(Genre.DIAMOND, CardNumber.QUEEN),
            Card(Genre.SPADE, CardNumber.QUEEN),
            Card(Genre.SPADE, CardNumber.JACK),
            Card(Genre.HEART, CardNumber.QUEEN),
            Card(Genre.CLUB, CardNumber.QUEEN),
        ]
        quads_QQQQJ = EvaluatorOf5Cards(stack)

        stack = [
            Card(Genre.DIAMOND, CardNumber.KING),
            Card(Genre.SPADE, CardNumber.KING),
            Card(Genre.SPADE, CardNumber.SEVEN),
            Card(Genre.HEART, CardNumber.KING),
            Card(Genre.CLUB, CardNumber.KING),
        ]
        quads_KKKK7 = EvaluatorOf5Cards(stack)
        self.assertEqual(quads_QQQQJ.getEvaluation(), Evaluation.FOUR_OF_A_KIND)
        self.assertEqual(quads_KKKK7.getEvaluation(), Evaluation.FOUR_OF_A_KIND)
        self.assertLess(quads_QQQQJ, quads_KKKK7)

        # quads are equal, high card dominates
        stack = [
            Card(Genre.DIAMOND, CardNumber.QUEEN),
            Card(Genre.SPADE, CardNumber.QUEEN),
            Card(Genre.SPADE, CardNumber.JACK),
            Card(Genre.HEART, CardNumber.QUEEN),
            Card(Genre.CLUB, CardNumber.QUEEN),
        ]
        quads_QQQQJ = EvaluatorOf5Cards(stack)

        stack = [
            Card(Genre.DIAMOND, CardNumber.QUEEN),
            Card(Genre.SPADE, CardNumber.QUEEN),
            Card(Genre.SPADE, CardNumber.SEVEN),
            Card(Genre.HEART, CardNumber.QUEEN),
            Card(Genre.CLUB, CardNumber.QUEEN),
        ]
        quads_QQQQ7 = EvaluatorOf5Cards(stack)
        self.assertEqual(quads_QQQQJ.getEvaluation(), Evaluation.FOUR_OF_A_KIND)
        self.assertEqual(quads_QQQQ7.getEvaluation(), Evaluation.FOUR_OF_A_KIND)
        self.assertLess(quads_QQQQ7, quads_QQQQJ)

    def test_comparisons_when_evaluations_are_straights(self):
        # 9TJQK < TJQKA
        stack = [
            Card(Genre.DIAMOND, CardNumber.KING),
            Card(Genre.SPADE, CardNumber.QUEEN),
            Card(Genre.SPADE, CardNumber.JACK),
            Card(Genre.HEART, CardNumber.TEN),
            Card(Genre.CLUB, CardNumber.NINE),
        ]
        straight_9TJQK = EvaluatorOf5Cards(stack)

        stack = [
            Card(Genre.DIAMOND, CardNumber.KING),
            Card(Genre.SPADE, CardNumber.QUEEN),
            Card(Genre.SPADE, CardNumber.JACK),
            Card(Genre.HEART, CardNumber.TEN),
            Card(Genre.CLUB, CardNumber.ACE),
        ]
        straight_TJQKA = EvaluatorOf5Cards(stack)
        self.assertEqual(straight_9TJQK.getEvaluation(), Evaluation.STRAIGHT)
        self.assertEqual(straight_TJQKA.getEvaluation(), Evaluation.STRAIGHT)
        self.assertLess(straight_9TJQK, straight_TJQKA)

        # A2345 < 23456
        stack = [
            Card(Genre.DIAMOND, CardNumber.TWO),
            Card(Genre.SPADE, CardNumber.THREE),
            Card(Genre.SPADE, CardNumber.FOUR),
            Card(Genre.HEART, CardNumber.FIVE),
            Card(Genre.CLUB, CardNumber.SIX),
        ]
        straight_23456 = EvaluatorOf5Cards(stack)

        stack = [
            Card(Genre.DIAMOND, CardNumber.TWO),
            Card(Genre.SPADE, CardNumber.THREE),
            Card(Genre.SPADE, CardNumber.FOUR),
            Card(Genre.HEART, CardNumber.FIVE),
            Card(Genre.CLUB, CardNumber.ACE),
        ]
        straight_A2345 = EvaluatorOf5Cards(stack)
        self.assertEqual(straight_23456.getEvaluation(), Evaluation.STRAIGHT)
        self.assertEqual(straight_A2345.getEvaluation(), Evaluation.STRAIGHT)
        self.assertLess(straight_A2345, straight_23456)

    def test_comparisons_when_evaluations_are_flush(self):
        stack = [
            Card(Genre.DIAMOND, CardNumber.KING),
            Card(Genre.DIAMOND, CardNumber.QUEEN),
            Card(Genre.DIAMOND, CardNumber.TWO),
            Card(Genre.DIAMOND, CardNumber.TEN),
            Card(Genre.DIAMOND, CardNumber.NINE),
        ]
        flush_KQT92 = EvaluatorOf5Cards(stack)

        stack = [
            Card(Genre.DIAMOND, CardNumber.THREE),
            Card(Genre.DIAMOND, CardNumber.FOUR),
            Card(Genre.DIAMOND, CardNumber.FIVE),
            Card(Genre.DIAMOND, CardNumber.SIX),
            Card(Genre.DIAMOND, CardNumber.ACE),
        ]
        flush_A6543 = EvaluatorOf5Cards(stack)
        self.assertEqual(flush_A6543.getEvaluation(), Evaluation.FLUSH)
        self.assertEqual(flush_KQT92.getEvaluation(), Evaluation.FLUSH)
        self.assertLess(flush_KQT92, flush_A6543)

    def test_comparisons_when_evaluations_are_straight_flush(self):
        # 34566 < 9TJQK
        stack = [
            Card(Genre.DIAMOND, CardNumber.KING),
            Card(Genre.DIAMOND, CardNumber.QUEEN),
            Card(Genre.DIAMOND, CardNumber.JACK),
            Card(Genre.DIAMOND, CardNumber.TEN),
            Card(Genre.DIAMOND, CardNumber.NINE),
        ]
        straight_flush_9TJQK = EvaluatorOf5Cards(stack)

        stack = [
            Card(Genre.SPADE, CardNumber.THREE),
            Card(Genre.SPADE, CardNumber.FOUR),
            Card(Genre.SPADE, CardNumber.FIVE),
            Card(Genre.SPADE, CardNumber.SIX),
            Card(Genre.SPADE, CardNumber.SEVEN),
        ]
        straight_flush_34567 = EvaluatorOf5Cards(stack)
        self.assertEqual(straight_flush_9TJQK.getEvaluation(), Evaluation.STRAIGHT_FLUSH)
        self.assertEqual(straight_flush_34567.getEvaluation(), Evaluation.STRAIGHT_FLUSH)
        self.assertLess(straight_flush_34567, straight_flush_9TJQK)

        # A2345 < 56789
        stack = [
            Card(Genre.DIAMOND, CardNumber.ACE),
            Card(Genre.DIAMOND, CardNumber.TWO),
            Card(Genre.DIAMOND, CardNumber.THREE),
            Card(Genre.DIAMOND, CardNumber.FOUR),
            Card(Genre.DIAMOND, CardNumber.FIVE),
        ]
        straight_flush_A2345 = EvaluatorOf5Cards(stack)

        stack = [
            Card(Genre.SPADE, CardNumber.FIVE),
            Card(Genre.SPADE, CardNumber.SIX),
            Card(Genre.SPADE, CardNumber.SEVEN),
            Card(Genre.SPADE, CardNumber.EIGHT),
            Card(Genre.SPADE, CardNumber.NINE),
        ]
        straight_flush_56789 = EvaluatorOf5Cards(stack)
        self.assertEqual(straight_flush_A2345.getEvaluation(), Evaluation.STRAIGHT_FLUSH)
        self.assertEqual(straight_flush_56789.getEvaluation(), Evaluation.STRAIGHT_FLUSH)
        self.assertLess(straight_flush_A2345, straight_flush_56789)

    def test_comparisons_when_evaluations_are_royal_straight_flush(self):
        # Royal straight flushes are all equal
        stack = [
            Card(Genre.DIAMOND, CardNumber.ACE),
            Card(Genre.DIAMOND, CardNumber.KING),
            Card(Genre.DIAMOND, CardNumber.QUEEN),
            Card(Genre.DIAMOND, CardNumber.JACK),
            Card(Genre.DIAMOND, CardNumber.TEN),
        ]
        royal_straight_flush_diamond = EvaluatorOf5Cards(stack)

        stack = [
            Card(Genre.SPADE, CardNumber.ACE),
            Card(Genre.SPADE, CardNumber.KING),
            Card(Genre.SPADE, CardNumber.QUEEN),
            Card(Genre.SPADE, CardNumber.JACK),
            Card(Genre.SPADE, CardNumber.TEN),
        ]
        royal_straight_flush_spade = EvaluatorOf5Cards(stack)
        self.assertEqual(royal_straight_flush_diamond.getEvaluation(), Evaluation.ROYAL_STRAIGHT_FLUSH)
        self.assertEqual(royal_straight_flush_spade.getEvaluation(), Evaluation.ROYAL_STRAIGHT_FLUSH)
        self.assertTrue(royal_straight_flush_diamond == royal_straight_flush_spade)
