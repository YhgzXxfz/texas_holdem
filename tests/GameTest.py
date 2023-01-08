import unittest

from cards.Card import Card, CardNumber, Genre
from evaluations.Evaluation import Evaluation
from games.Deck import Deck
from games.Game import Game
from players.Player import ID_generator, Player
from players.Policy import Policy


class GameTest(unittest.TestCase):
    def setUp(self) -> None:
        return super().setUp()

    # --------------------- Player Seats ------------------------
    def test_players_sit_in_right_place(self):
        # Given
        game = Game()
        harry = Player("Harry Potter", ID=ID_generator(), money=3)
        tom = Player("Tom Dwan", ID=ID_generator(), money=5)
        phil = Player("Phil Ivey", ID=ID_generator(), money=1)

        # When
        tom.join_game(game, position=4)
        harry.join_game(game, position=1)
        phil.join_game(game, position=0)

        # Then
        self.assertTrue(len(game.player_list) == 3)
        self.assertTrue(game.get_players_in_the_game() == [phil, harry, tom])

    def test_cannot_sit_on_a_place_taken(self):
        # Given
        game = Game()
        harry = Player("Harry Potter", ID=ID_generator(), money=3)
        harry.join_game(game, position=1)

        # When
        phil = Player("Phil Ivey", ID=ID_generator(), money=1)

        # Then
        self.assertRaises(KeyError, phil.join_game, game, 1)

    # --------------------------- Deck ----------------------------
    def test_deck_is_initialized(self):
        # Given, When
        deck = Deck()

        # Then
        cards = [Card(g, n) for g in Genre for n in CardNumber]
        self.assertNotEqual(cards, deck.cards)
        self.assertEqual(set(cards), set(deck.cards))

    def test_skip_one_card_in_deck(self):
        # Given
        deck = Deck()

        # When
        deck.skip_one_card()

        # Then
        self.assertTrue(deck.peek_top_card() == deck.cards[1])

    def test_pop_cards_from_deck(self):
        # Given
        deck = Deck()

        # When
        deck.skip_one_card()
        deck.pop_cards(3)
        deck.skip_one_card()
        cards = deck.pop_cards(2)

        # Then
        self.assertTrue(len(cards) == 2)
        self.assertEqual(deck.cards[5:7], list(cards))

    # --------------------------- Game ----------------------------
    def test_game_ends_after_preflop(self):
        # Given
        game = Game()
        tom = Player("Tom Dwan", ID=ID_generator(), money=50, policy=Policy.ALWAYS_CHECK_OR_FOLD)
        tom.join_game(game, position=3)
        harry = Player("Harry Potter", ID=ID_generator(), money=300, policy=Policy.ALWAYS_CALL)
        harry.join_game(game, position=1)
        anton = Player("Anton Dom", ID=ID_generator(), money=1000, policy=Policy.ALWAYS_CHECK_OR_FOLD)
        anton.join_game(game, position=4)
        phil = Player("Phil Ivey", ID=ID_generator(), money=150, policy=Policy.ALWAYS_CHECK_OR_FOLD)
        phil.join_game(game, position=0)

        # When
        game.start()

        # Then
        self.assertTrue(game.deck.index == 8)
        self.assertTrue(game.pot.compute_total_sum() == 0)
        self.assertTrue(phil.money == 149)
        self.assertTrue(harry.money == 301)
        self.assertTrue(tom.money == 50)
        self.assertTrue(anton.money == 1_000)

    def test_game_goes_to_comparison_after_river_if_there_are_more_than_one_player_remained(self):
        # Given
        game = Game()
        tom = Player("Tom Dwan", ID=ID_generator(), money=50, policy=Policy.ALWAYS_CHECK_OR_FOLD)
        tom.join_game(game, position=3)
        harry = Player("Harry Potter", ID=ID_generator(), money=300, policy=Policy.ALWAYS_CALL)
        harry.join_game(game, position=1)
        anton = Player("Anton Dom", ID=ID_generator(), money=1000, policy=Policy.ALWAYS_CALL)
        anton.join_game(game, position=4)
        phil = Player("Phil Ivey", ID=ID_generator(), money=150, policy=Policy.ALWAYS_CHECK_OR_FOLD)
        phil.join_game(game, position=0)

        # When
        game.start()

        # Then
        self.assertTrue(game.deck.index == 16)
        self.assertTrue(game.pot.compute_total_sum() == 5)
        self.assertTrue(phil.money == 149)
        self.assertTrue(harry.money == 298)
        self.assertTrue(tom.money == 50)
        self.assertTrue(anton.money == 998)

    def test_showdown_with_distinct_optimal_hands(self):
        # Given
        game = Game()
        tom = Player("Tom Dwan", ID=ID_generator(), money=50, policy=Policy.ALWAYS_CHECK_OR_FOLD)
        tom.join_game(game, position=3)
        harry = Player("Harry Potter", ID=ID_generator(), money=300, policy=Policy.ALWAYS_CALL)
        harry.join_game(game, position=1)
        anton = Player("Anton Dom", ID=ID_generator(), money=1000, policy=Policy.ALWAYS_CALL)
        anton.join_game(game, position=4)
        phil = Player("Phil Ivey", ID=ID_generator(), money=150, policy=Policy.ALWAYS_CHECK_OR_FOLD)
        phil.join_game(game, position=0)

        phil.pocket_cards = (
            Card(Genre.DIAMOND, CardNumber.QUEEN),
            Card(Genre.CLUB, CardNumber.QUEEN),
        )
        harry.pocket_cards = (
            Card(Genre.HEART, CardNumber.QUEEN),
            Card(Genre.CLUB, CardNumber.JACK),
        )
        tom.pocket_cards = (
            Card(Genre.SPADE, CardNumber.SEVEN),
            Card(Genre.SPADE, CardNumber.EIGHT),
        )
        anton.pocket_cards = (
            Card(Genre.CLUB, CardNumber.THREE),
            Card(Genre.CLUB, CardNumber.FOUR),
        )

        community_cards = [
            Card(Genre.SPADE, CardNumber.QUEEN),
            Card(Genre.SPADE, CardNumber.TWO),
            Card(Genre.DIAMOND, CardNumber.JACK),
            Card(Genre.HEART, CardNumber.ACE),
            Card(Genre.SPADE, CardNumber.FIVE),
        ]

        # When
        evaluation_order = game.showdown(community_cards, [phil, harry, tom, anton])

        # Then
        self.assertTrue(len(evaluation_order) == 4)
        self.assertTrue(
            [eva.get_evaluation() for eva in evaluation_order.keys()]
            == [Evaluation.FLUSH, Evaluation.STRAIGHT, Evaluation.THREE_OF_A_KIND, Evaluation.TWO_PAIRS]
        )
        self.assertTrue(list(evaluation_order.values()) == [[tom], [anton], [phil], [harry]])

    def test_showdown_with_same_optimal_hands(self):
        # Given
        game = Game()
        tom = Player("Tom Dwan", ID=ID_generator(), money=50, policy=Policy.ALWAYS_CHECK_OR_FOLD)
        tom.join_game(game, position=3)
        harry = Player("Harry Potter", ID=ID_generator(), money=300, policy=Policy.ALWAYS_CALL)
        harry.join_game(game, position=1)
        anton = Player("Anton Dom", ID=ID_generator(), money=1000, policy=Policy.ALWAYS_CALL)
        anton.join_game(game, position=4)
        phil = Player("Phil Ivey", ID=ID_generator(), money=150, policy=Policy.ALWAYS_CHECK_OR_FOLD)
        phil.join_game(game, position=0)

        phil.pocket_cards = (
            Card(Genre.DIAMOND, CardNumber.QUEEN),
            Card(Genre.CLUB, CardNumber.QUEEN),
        )
        harry.pocket_cards = (
            Card(Genre.HEART, CardNumber.QUEEN),
            Card(Genre.CLUB, CardNumber.JACK),
        )
        tom.pocket_cards = (
            Card(Genre.HEART, CardNumber.THREE),
            Card(Genre.HEART, CardNumber.FOUR),
        )
        anton.pocket_cards = (
            Card(Genre.CLUB, CardNumber.THREE),
            Card(Genre.CLUB, CardNumber.FOUR),
        )

        community_cards = [
            Card(Genre.SPADE, CardNumber.QUEEN),
            Card(Genre.SPADE, CardNumber.TWO),
            Card(Genre.DIAMOND, CardNumber.JACK),
            Card(Genre.HEART, CardNumber.ACE),
            Card(Genre.SPADE, CardNumber.FIVE),
        ]

        # When
        evaluation_order = game.showdown(community_cards, [phil, harry, tom, anton])

        # Then
        self.assertTrue(len(evaluation_order) == 3)
        self.assertTrue(
            [eva.get_evaluation() for eva in evaluation_order.keys()]
            == [Evaluation.STRAIGHT, Evaluation.THREE_OF_A_KIND, Evaluation.TWO_PAIRS]
        )
        self.assertTrue(list(evaluation_order.values()) == [[tom, anton], [phil], [harry]])
