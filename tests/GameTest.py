import random
import unittest

from cards.Card import Card, CardNumber, Genre
from evaluations.Evaluation import Evaluation
from evaluations.EvaluatorOf5Cards import EvaluatorOf5Cards
from games.Deck import Deck
from games.Game import Game
from players.Player import ID_generator, Player
from players.Policy import Policy
from rounds.Pot import Pot
from rounds.RoundName import RoundName


class GameTest(unittest.TestCase):
    def setUp(self) -> None:
        unittest.TextTestRunner(verbosity=2)
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
        # This seed determines the Deck and there for is responsible for the winner.
        random.seed(1)

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
        self.assertTrue(harry.money == 303)
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
            Card(Genre.SPADE, CardNumber.THREE),
            Card(Genre.SPADE, CardNumber.FOUR),
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
            == [Evaluation.FLUSH, Evaluation.FLUSH, Evaluation.THREE_OF_A_KIND, Evaluation.TWO_PAIRS]
        )
        self.assertTrue(list(evaluation_order.values()) == [[tom], [anton], [phil], [harry]])

    def test_showdown_with_same_optimal_hands(self):
        # Given
        game = Game()
        tom = Player("Tom Dwan", ID=ID_generator(), money=50, policy=Policy.ALWAYS_CALL)
        tom.join_game(game, position=4)
        harry = Player("Harry Potter", ID=ID_generator(), money=300, policy=Policy.ALWAYS_CALL)
        harry.join_game(game, position=1)
        anton = Player("Anton Dom", ID=ID_generator(), money=1000, policy=Policy.ALWAYS_CALL)
        anton.join_game(game, position=3)
        phil = Player("Phil Ivey", ID=ID_generator(), money=150, policy=Policy.ALWAYS_CALL)
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
        game.pot = Pot()
        game.pot.roundpots = {
            RoundName.PREFLOP: {phil: 10, harry: 10, tom: 10, anton: 10},
            RoundName.FLOP: {phil: 10, harry: 10, tom: 10, anton: 10},
            RoundName.TURN: {phil: 0, harry: 0, tom: 0, anton: 0},
            RoundName.RIVER: {phil: 50, harry: 50, tom: 30, anton: 50},
        }

        # When
        evaluation_order = game.showdown(community_cards, game.get_players_in_the_game())

        # Then
        self.assertTrue(len(evaluation_order) == 3)
        self.assertTrue(
            [eva.get_evaluation() for eva in evaluation_order.keys()]
            == [Evaluation.STRAIGHT, Evaluation.THREE_OF_A_KIND, Evaluation.TWO_PAIRS]
        )
        self.assertTrue(list(evaluation_order.values()) == [[tom, anton], [phil], [harry]])

    def test_settle_showdown_with_all_in_and_side_pots(self) -> None:
        # Given
        game = Game()

        patrick = Player("Patrick Antonius", ID=ID_generator(), money=1_000, policy=Policy.ALWAYS_CALL)
        patrick.join_game(game, position=2)
        allen = Player("Allen Baggio", ID=ID_generator(), money=1_000, policy=Policy.ALWAYS_CALL)
        allen.join_game(game, position=5)
        tom = Player("Tom Dwan", ID=ID_generator(), money=65, policy=Policy.ALWAYS_CALL)
        tom.join_game(game, position=4)
        harry = Player("Harry Potter", ID=ID_generator(), money=135, policy=Policy.ALWAYS_CALL)
        harry.join_game(game, position=1)
        anton = Player("Anton Dom", ID=ID_generator(), money=1_000, policy=Policy.ALWAYS_CALL)
        anton.join_game(game, position=3)
        phil = Player("Phil Ivey", ID=ID_generator(), money=85, policy=Policy.ALWAYS_CALL)
        phil.join_game(game, position=0)

        # Simulate betting
        game.pot = Pot()
        game.pot.roundpots = {
            RoundName.PREFLOP: {phil: 10, harry: 10, patrick: 10, anton: 10, tom: 10, allen: 10},
            RoundName.FLOP: {phil: 25, harry: 25, patrick: 0, anton: 25, tom: 25, allen: 0},
            RoundName.TURN: {phil: 0, harry: 0, patrick: 0, anton: 0, tom: 0, allen: 0},
            RoundName.RIVER: {phil: 50, harry: 100, patrick: 0, anton: 200, tom: 30, allen: 0},
        }
        for p in game.get_players_in_the_game():
            p.money -= game.pot.get_chips_for(p)

        # Simulate hands
        eva_to_players = {
            EvaluatorOf5Cards(
                [
                    Card(Genre.CLUB, CardNumber.ACE),
                    Card(Genre.SPADE, CardNumber.ACE),
                    Card(Genre.DIAMOND, CardNumber.QUEEN),
                    Card(Genre.DIAMOND, CardNumber.ACE),
                    Card(Genre.HEART, CardNumber.ACE),
                ]
            ): [tom],
            EvaluatorOf5Cards(
                [
                    Card(Genre.CLUB, CardNumber.ACE),
                    Card(Genre.SPADE, CardNumber.ACE),
                    Card(Genre.CLUB, CardNumber.KING),
                    Card(Genre.HEART, CardNumber.KING),
                    Card(Genre.HEART, CardNumber.JACK),
                ]
            ): [phil, harry],
            EvaluatorOf5Cards(
                [
                    Card(Genre.CLUB, CardNumber.ACE),
                    Card(Genre.SPADE, CardNumber.ACE),
                    Card(Genre.DIAMOND, CardNumber.QUEEN),
                    Card(Genre.CLUB, CardNumber.KING),
                    Card(Genre.HEART, CardNumber.QUEEN),
                ]
            ): [anton],
        }

        # When
        iteration = game.settle_showdown(eva_to_players)

        # Then
        self.assertTrue(iteration == 4, "One iteration per player.")
        self.assertTrue(tom.money == 65 + 65 + 10 + 65 + 65 + 10)
        self.assertTrue(phil.money == 20 + 20 // 2)
        self.assertTrue(harry.money == (20 + 20 // 2) + (50 + 50 // 1))
        self.assertTrue(anton.money == 865)
        self.assertTrue(patrick.money == 990)
        self.assertTrue(allen.money == 990)

    def test_settle_showdown_with_remainders(self) -> None:
        # Given
        game = Game()

        patrick = Player("Patrick Antonius", ID=ID_generator(), money=1_000, policy=Policy.ALWAYS_CALL)
        patrick.join_game(game, position=2)
        allen = Player("Allen Baggio", ID=ID_generator(), money=1_000, policy=Policy.ALWAYS_CALL)
        allen.join_game(game, position=5)
        tom = Player("Tom Dwan", ID=ID_generator(), money=65, policy=Policy.ALWAYS_CALL)
        tom.join_game(game, position=4)
        harry = Player("Harry Potter", ID=ID_generator(), money=135, policy=Policy.ALWAYS_CALL)
        harry.join_game(game, position=1)
        anton = Player("Anton Dom", ID=ID_generator(), money=1_000, policy=Policy.ALWAYS_CALL)
        anton.join_game(game, position=3)
        phil = Player("Phil Ivey", ID=ID_generator(), money=85, policy=Policy.ALWAYS_CALL)
        phil.join_game(game, position=0)

        # Simulate betting
        game.pot = Pot()
        game.pot.roundpots = {
            RoundName.PREFLOP: {phil: 10, harry: 10, patrick: 10, anton: 10, tom: 10, allen: 10},
            RoundName.FLOP: {phil: 25, harry: 25, patrick: 0, anton: 25, tom: 25, allen: 0},
            RoundName.TURN: {phil: 0, harry: 0, patrick: 0, anton: 0, tom: 0, allen: 0},
            RoundName.RIVER: {phil: 50, harry: 100, patrick: 0, anton: 200, tom: 30, allen: 0},
        }
        for p in game.get_players_in_the_game():
            p.money -= game.pot.get_chips_for(p)

        # Simulate hands
        eva_to_players = {
            EvaluatorOf5Cards(
                [
                    Card(Genre.CLUB, CardNumber.ACE),
                    Card(Genre.SPADE, CardNumber.KING),
                    Card(Genre.DIAMOND, CardNumber.QUEEN),
                    Card(Genre.DIAMOND, CardNumber.JACK),
                    Card(Genre.HEART, CardNumber.TEN),
                ]
            ): [tom, phil, harry],
            EvaluatorOf5Cards(
                [
                    Card(Genre.CLUB, CardNumber.ACE),
                    Card(Genre.SPADE, CardNumber.ACE),
                    Card(Genre.DIAMOND, CardNumber.QUEEN),
                    Card(Genre.CLUB, CardNumber.KING),
                    Card(Genre.HEART, CardNumber.QUEEN),
                ]
            ): [anton],
        }

        # When
        iteration = game.settle_showdown(eva_to_players)

        # Then
        self.assertTrue(iteration == 4, "One iteration per player.")
        self.assertTrue(
            tom.money == 65 + (0 + 0 + 10 + 65 + 0 + 10) // 3,
            "Tom bets the smallest and goes with the 1st side pot to share with 2 other players.",
        )
        self.assertTrue(
            harry.money
            == 65
            + (0 + 0 + 10 + 65 + 0 + 10) // 3
            + 20
            + (0 + 0 + 0 + 20 + 0 + 0) // 2
            + 50
            + (0 + 0 + 0 + 50 + 0 + 0) // 1,
            "Harry bets 3rd smallest and goes with 1st, 2nd, 3rd side pot of 3, 2, 1 players respectively.",
        )
        self.assertTrue(anton.money == 865)
        self.assertTrue(
            phil.money
            == 65
            + (0 + 0 + 10 + 65 + 0 + 10) // 3
            + 20
            + (0 + 0 + 0 + 20 + 0 + 0) // 2
            + (0 + 0 + 10 + 65 + 0 + 10) % 3  # Don't forget remainders
            + (0 + 0 + 0 + 20 + 0 + 0) % 2
            + (0 + 0 + 0 + 50 + 0 + 0) % 1,
            "Phil bets 2nd smallest and goes with 1st, 2nd side pot of 3 and 2 players respectively.",
        )
        self.assertTrue(patrick.money == 990)
        self.assertTrue(allen.money == 990)

    def test_settle_showdown_with_side_pots_with_one_pot_where_players_put_the_same_bet(self) -> None:
        # Given
        game = Game()

        patrick = Player("Patrick Antonius", ID=ID_generator(), money=1_000, policy=Policy.ALWAYS_CALL)
        patrick.join_game(game, position=2)
        allen = Player("Allen Baggio", ID=ID_generator(), money=1_000, policy=Policy.ALWAYS_CALL)
        allen.join_game(game, position=5)
        tom = Player("Tom Dwan", ID=ID_generator(), money=65, policy=Policy.ALWAYS_CALL)
        tom.join_game(game, position=4)
        harry = Player("Harry Potter", ID=ID_generator(), money=85, policy=Policy.ALWAYS_CALL)
        harry.join_game(game, position=1)
        anton = Player("Anton Dom", ID=ID_generator(), money=1_000, policy=Policy.ALWAYS_CALL)
        anton.join_game(game, position=3)
        phil = Player("Phil Ivey", ID=ID_generator(), money=85, policy=Policy.ALWAYS_CALL)
        phil.join_game(game, position=0)

        # Simulate betting
        game.pot = Pot()
        game.pot.roundpots = {
            RoundName.PREFLOP: {phil: 10, harry: 10, patrick: 10, anton: 10, tom: 10, allen: 10},
            RoundName.FLOP: {phil: 25, harry: 25, patrick: 0, anton: 25, tom: 25, allen: 0},
            RoundName.TURN: {phil: 0, harry: 0, patrick: 0, anton: 0, tom: 0, allen: 0},
            RoundName.RIVER: {phil: 50, harry: 50, patrick: 0, anton: 200, tom: 30, allen: 0},
        }  # Phil and Harry bet the same
        for p in game.get_players_in_the_game():
            p.money -= game.pot.get_chips_for(p)

        # Simulate hands
        eva_to_players = {
            EvaluatorOf5Cards(
                [
                    Card(Genre.CLUB, CardNumber.ACE),
                    Card(Genre.SPADE, CardNumber.ACE),
                    Card(Genre.DIAMOND, CardNumber.QUEEN),
                    Card(Genre.DIAMOND, CardNumber.ACE),
                    Card(Genre.HEART, CardNumber.ACE),
                ]
            ): [tom],
            EvaluatorOf5Cards(
                [
                    Card(Genre.CLUB, CardNumber.ACE),
                    Card(Genre.SPADE, CardNumber.ACE),
                    Card(Genre.CLUB, CardNumber.KING),
                    Card(Genre.HEART, CardNumber.KING),
                    Card(Genre.HEART, CardNumber.JACK),
                ]
            ): [
                phil,
                harry,
            ],  # Phil and Harry are in the same pot
            EvaluatorOf5Cards(
                [
                    Card(Genre.CLUB, CardNumber.ACE),
                    Card(Genre.SPADE, CardNumber.ACE),
                    Card(Genre.DIAMOND, CardNumber.QUEEN),
                    Card(Genre.CLUB, CardNumber.KING),
                    Card(Genre.HEART, CardNumber.QUEEN),
                ]
            ): [anton],
        }

        # When
        iteration = game.settle_showdown(eva_to_players)

        # Then
        self.assertTrue(iteration == 3, "2nd side pot has two players with same bets and should have 1 iteration.")
        self.assertTrue(tom.money == 65 + 65 + 10 + 65 + 65 + 10, "1st side pot")
        self.assertTrue(phil.money == 20 + 20 // 2, "2nd side pot.")
        self.assertTrue(harry.money == 20 + 20 // 2, "2nd side pot.")
        self.assertTrue(anton.money == 915)
        self.assertTrue(patrick.money == 990)
        self.assertTrue(allen.money == 990)

    def test_settle_showdown_where_players_with_the_best_hands_bet_the_most(self) -> None:
        # Given
        game = Game()

        patrick = Player("Patrick Antonius", ID=ID_generator(), money=1_000, policy=Policy.ALWAYS_CALL)
        patrick.join_game(game, position=2)
        allen = Player("Allen Baggio", ID=ID_generator(), money=1_000, policy=Policy.ALWAYS_CALL)
        allen.join_game(game, position=5)
        tom = Player("Tom Dwan", ID=ID_generator(), money=65, policy=Policy.ALWAYS_CALL)
        tom.join_game(game, position=4)
        harry = Player("Harry Potter", ID=ID_generator(), money=135, policy=Policy.ALWAYS_CALL)
        harry.join_game(game, position=1)
        anton = Player("Anton Dom", ID=ID_generator(), money=1_000, policy=Policy.ALWAYS_CALL)
        anton.join_game(game, position=3)
        phil = Player("Phil Ivey", ID=ID_generator(), money=85, policy=Policy.ALWAYS_CALL)
        phil.join_game(game, position=0)

        # Simulate betting
        game.pot = Pot()
        game.pot.roundpots = {
            RoundName.PREFLOP: {phil: 10, harry: 10, patrick: 10, anton: 10, tom: 10, allen: 10},
            RoundName.FLOP: {phil: 25, harry: 25, patrick: 0, anton: 25, tom: 25, allen: 0},
            RoundName.TURN: {phil: 0, harry: 0, patrick: 0, anton: 0, tom: 0, allen: 0},
            RoundName.RIVER: {phil: 50, harry: 100, patrick: 0, anton: 200, tom: 30, allen: 0},
        }  # Phil and Harry bet the same
        for p in game.get_players_in_the_game():
            p.money -= game.pot.get_chips_for(p)

        # Simulate hands
        eva_to_players = {
            EvaluatorOf5Cards(
                [
                    Card(Genre.CLUB, CardNumber.ACE),
                    Card(Genre.SPADE, CardNumber.ACE),
                    Card(Genre.DIAMOND, CardNumber.QUEEN),
                    Card(Genre.DIAMOND, CardNumber.ACE),
                    Card(Genre.HEART, CardNumber.ACE),
                ]
            ): [anton],
            EvaluatorOf5Cards(
                [
                    Card(Genre.CLUB, CardNumber.ACE),
                    Card(Genre.SPADE, CardNumber.ACE),
                    Card(Genre.DIAMOND, CardNumber.QUEEN),
                    Card(Genre.CLUB, CardNumber.KING),
                    Card(Genre.HEART, CardNumber.QUEEN),
                ]
            ): [tom, phil, harry],
        }

        # When
        iteration = game.settle_showdown(eva_to_players)

        # Then
        self.assertTrue(iteration == 1, "Should finish calculation once the 1st side pot is settled.")
        self.assertTrue(anton.money == 85 + 135 + 10 + 1_000 + 65 + 10, "1st side pot")
        self.assertTrue(tom.money == 0, "2nd side pot")
        self.assertTrue(phil.money == 0, "2nd side pot.")
        self.assertTrue(harry.money == 0, "2nd side pot.")
        self.assertTrue(patrick.money == 990)
        self.assertTrue(allen.money == 990)
