import unittest

from games.Game import Game
from players.Player import ID_generator, Player
from players.Policy import Policy
from rounds.Round import Preflop
from rounds.RoundName import RoundName


class PreflopRoundTest(unittest.TestCase):
    def setUp(self) -> None:
        self.game = Game()
        self.tom = Player("Tom Dwan", ID=ID_generator(), money=50, policy=Policy.ALWAYS_CALL)
        self.tom.join_game(self.game, position=3)
        self.harry = Player("Harry Potter", ID=ID_generator(), money=300, policy=Policy.ALWAYS_CALL)
        self.harry.join_game(self.game, position=1)
        self.anton = Player("Anton Dom", ID=ID_generator(), money=1000, policy=Policy.ALWAYS_CHECK_OR_FOLD)
        self.anton.join_game(self.game, position=4)
        self.phil = Player("Phil Ivey", ID=ID_generator(), money=150, policy=Policy.ALWAYS_CALL)
        self.phil.join_game(self.game, position=0)

    def test_initialize_preflop(self):
        # When
        preflop = Preflop(
            players=self.game.get_players_in_the_game(),
            deck=self.game.deck,
            pot=self.game.pot,
        )

        # Then
        # Players have bet small and big blines
        self.assertTrue(self.phil.money == 149)
        self.assertTrue(self.harry.money == 298)
        self.assertTrue(self.tom.money == 50)
        self.assertTrue(self.anton.money == 1_000)

        # pot is initialized
        self.assertTrue(len(self.game.pot.roundpots[RoundName.PREFLOP]) == 4)
        self.assertEqual(
            self.game.pot.roundpots[RoundName.PREFLOP], {self.phil: 1, self.harry: 2, self.tom: 0, self.anton: 0}
        )
        self.assertTrue(self.game.pot.compute_total_sum() == 3)
        self.assertFalse(self.game.pot.is_balanced(RoundName.PREFLOP))

        # hands are distributed correctly
        self.assertTrue(self.game.deck.index == 8)
        self.assertTrue({self.game.deck.cards[0], self.game.deck.cards[4]} == set(self.phil.pocket_cards))
        self.assertTrue({self.game.deck.cards[1], self.game.deck.cards[5]} == set(self.harry.pocket_cards))
        self.assertTrue({self.game.deck.cards[2], self.game.deck.cards[6]} == set(self.tom.pocket_cards))
        self.assertTrue({self.game.deck.cards[3], self.game.deck.cards[7]} == set(self.anton.pocket_cards))

        # Rund has not started
        self.assertTrue(preflop.check_round_result() == [])

    def test_preflop_result_when_all_players_but_one_fold(self):
        # When
        preflop = Preflop(
            players=self.game.get_players_in_the_game(),
            deck=self.game.deck,
            pot=self.game.pot,
        )
        self.phil.fold()
        self.tom.fold()
        self.anton.fold()

        # Then
        self.assertTrue(self.phil.money == 149)
        self.assertTrue(self.tom.money == 50)
        self.assertTrue(self.anton.money == 1_000)
        self.assertFalse(self.game.pot.is_balanced(RoundName.PREFLOP))
        self.assertTrue(preflop.check_round_result() == [self.harry])

    def test_preflop_pot_is_not_finished_before_big_blind_takes_action(self):
        # When
        preflop = Preflop(
            players=self.game.get_players_in_the_game(),
            deck=self.game.deck,
            pot=self.game.pot,
        )
        self.tom.fold()
        self.anton.fold()
        self.phil.call(self.game.pot, roundname=RoundName.PREFLOP)

        # Then
        self.assertTrue(self.phil.money == 148)
        self.assertTrue(self.tom.money == 50)
        self.assertTrue(self.anton.money == 1_000)
        self.assertTrue(self.game.pot.is_balanced(RoundName.PREFLOP))
        self.assertTrue(preflop.check_round_result() == [], "round is not finished.")

    def test_preflop_pot_is_terminated_when_everyone_calls_and_big_blind_checks(self):
        # When
        preflop = Preflop(
            players=self.game.get_players_in_the_game(),
            deck=self.game.deck,
            pot=self.game.pot,
        )
        self.tom.fold()
        self.anton.fold()
        self.phil.call(self.game.pot, roundname=RoundName.PREFLOP)
        self.harry.check()

        # Then
        self.assertTrue(self.phil.money == 148)
        self.assertTrue(self.tom.money == 50)
        self.assertTrue(self.anton.money == 1_000)
        self.assertTrue(self.game.pot.is_balanced(RoundName.PREFLOP))
        self.assertTrue(preflop.check_round_result() == [self.phil, self.harry])

    def test_preflop_pot_is_unbalanced_when_one_raises(self):
        # When
        preflop = Preflop(
            players=self.game.get_players_in_the_game(),
            deck=self.game.deck,
            pot=self.game.pot,
        )
        self.tom.fold()
        self.anton.fold()
        self.phil.bet(self.game.pot, RoundName.PREFLOP, 9)

        # Then
        self.assertTrue(self.phil.money == 140)
        self.assertTrue(self.tom.money == 50)
        self.assertTrue(self.anton.money == 1_000)
        self.assertFalse(self.game.pot.is_balanced(RoundName.PREFLOP))
        self.assertTrue(preflop.check_round_result() == [], "round is not finished.")

    def test_preflop_pot_is_balanced_when_everyone_in_the_game_puts_the_same_chips(self):
        # When
        preflop = Preflop(
            players=self.game.get_players_in_the_game(),
            deck=self.game.deck,
            pot=self.game.pot,
        )
        self.tom.fold()
        self.anton.fold()
        self.phil.bet(self.game.pot, RoundName.PREFLOP, 9)
        self.harry.call(self.game.pot, RoundName.PREFLOP)

        # Then
        self.assertTrue(self.phil.money == 140)
        self.assertTrue(self.harry.money == 290)
        self.assertTrue(self.tom.money == 50)
        self.assertTrue(self.anton.money == 1_000)
        self.assertTrue(self.game.pot.is_balanced(RoundName.PREFLOP))
        self.assertTrue(preflop.check_round_result() == [self.phil, self.harry])

    def test_preflop_pot_is_balanced_when_one_is_all_in(self):
        # When
        preflop = Preflop(
            players=self.game.get_players_in_the_game(),
            deck=self.game.deck,
            pot=self.game.pot,
        )
        self.tom.fold()
        self.anton.fold()
        self.phil.bet(self.game.pot, RoundName.PREFLOP, 9)
        self.harry.bet(self.game.pot, RoundName.PREFLOP, 200)
        self.phil.call(self.game.pot, RoundName.PREFLOP)

        # Then
        self.assertTrue(self.phil.money == 0)
        self.assertTrue(self.harry.money == 98)
        self.assertTrue(self.tom.money == 50)
        self.assertTrue(self.anton.money == 1_000)
        self.assertTrue(self.game.pot.is_balanced(RoundName.PREFLOP))
        self.assertTrue(self.game.pot.compute_total_sum() == 150 + 202)
        self.assertTrue(preflop.check_round_result() == [self.phil, self.harry])

    def test_run_preflop(self):
        # When
        preflop = Preflop(
            players=self.game.get_players_in_the_game(),
            deck=self.game.deck,
            pot=self.game.pot,
        )
        result = preflop.run()

        # Then
        self.assertTrue(self.phil.money == 148)
        self.assertTrue(self.harry.money == 298)
        self.assertTrue(self.tom.money == 48)
        self.assertTrue(self.anton.money == 1_000)
        self.assertTrue(self.game.pot.is_balanced(RoundName.PREFLOP))
        self.assertTrue(result == [self.phil, self.harry, self.tom])
