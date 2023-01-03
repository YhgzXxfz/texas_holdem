import unittest

from cards.Card import Card, CardNumber, Genre
from games.Deck import Deck
from games.Game import Game
from players.Player import ID_generator, Player
from rounds.Pot import Pot
from rounds.Round import Preflop


class GameTest(unittest.TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def test_players_sit_in_right_place(self):
        # Given
        game = Game()
        harry = Player("Harry Potter", ID=ID_generator(), money=3)
        tom = Player("Tom Dwan", ID=ID_generator(), money=5)
        phil = Player("Phil Ivey", ID=ID_generator(), money=1)

        # When
        harry.join_game(game, position=1)
        tom.join_game(game, position=4)
        phil.join_game(game, position=0)

        # Then
        self.assertTrue(len(game.player_list) == 3)
        self.assertTrue(game.player_list[0].name == "Phil Ivey")
        self.assertTrue(game.player_list[1].name == "Harry Potter")
        self.assertTrue(game.player_list[2].name == "Tom Dwan")

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

    def test_initialize_preflop(self):
        # Given
        deck = Deck()
        phil = Player("Phil Ivey", ID=ID_generator(), money=150)
        harry = Player("Harry Potter", ID=ID_generator(), money=300)
        pot = Pot()

        # When
        Preflop(players=(phil, harry), deck=deck, pot=pot, small_blind=1, big_blind=2)

        # Then
        # hands are distributed correctly
        self.assertTrue(deck.index == 4)
        self.assertTrue({deck.cards[0], deck.cards[2]}, set(phil.hands))
        self.assertTrue({deck.cards[1], deck.cards[3]}, set(harry.hands))

        # pot is initialized
        self.assertTrue(len(pot.preflop) == 2)
        self.assertEqual(pot.preflop, {phil: 1, harry: 2})
        self.assertTrue(pot.compute_total_sum() == 3)
