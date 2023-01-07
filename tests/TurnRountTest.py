import unittest

from games.Game import Game
from players.Player import ID_generator, Player
from players.Policy import Policy
from rounds.Round import Flop, Preflop, Turn
from rounds.RoundName import RoundName


class TurnRoundTest(unittest.TestCase):
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

        preflop = Preflop(
            players=self.game.get_players_in_the_game(),
            deck=self.game.deck,
            pot=self.game.pot,
            small_blind=1,
            big_blind=2,
        )

        self.tom.call(self.game.pot, roundname=RoundName.PREFLOP)
        self.anton.fold()
        self.phil.fold()
        self.harry.check()

        self.flop = Flop(players=preflop.check_round_result(), deck=self.game.deck, pot=self.game.pot)
        self.harry.check()
        self.tom.check()

    def test_initialize_turn(self):
        # When
        turn = Turn(players=self.flop.check_round_result(), deck=self.game.deck, pot=self.game.pot)

        # Then
        self.assertTrue(self.game.deck.index == 14, "Turn cards should be displayed")
        self.assertTrue(self.phil.money == 149)
        self.assertTrue(self.harry.money == 298)
        self.assertTrue(self.tom.money == 48)
        self.assertTrue(self.anton.money == 1_000)
        self.assertTrue(self.game.pot.compute_total_sum() == 5)
        self.assertTrue(turn.check_round_result() == [], "round has not started")

    def test_turn_pot_is_unbalanced_when_one_raises(self):
        # When
        turn = Turn(players=self.flop.check_round_result(), deck=self.game.deck, pot=self.game.pot)
        self.harry.bet(self.game.pot, RoundName.TURN, 9)

        # Then
        self.assertTrue(self.phil.money == 149)
        self.assertTrue(self.harry.money == 289)
        self.assertTrue(self.tom.money == 48)
        self.assertTrue(self.anton.money == 1_000)
        self.assertTrue(self.game.pot.compute_total_sum() == 14)
        self.assertFalse(self.game.pot.is_balanced(RoundName.TURN))
        self.assertTrue(turn.check_round_result() == [], "round is not finished.")

    def test_turn_pot_is_balanced_when_everyone_calls(self):
        # Given
        turn = Turn(players=self.flop.check_round_result(), deck=self.game.deck, pot=self.game.pot)

        # When
        self.harry.bet(self.game.pot, roundname=RoundName.TURN, to_putin=5)
        self.tom.call(self.game.pot, roundname=RoundName.TURN)

        # Then
        self.assertTrue(self.phil.money == 149)
        self.assertTrue(self.harry.money == 293)
        self.assertTrue(self.tom.money == 43)
        self.assertTrue(self.anton.money == 1_000)
        self.assertTrue(self.game.pot.compute_total_sum() == 15)
        self.assertTrue(self.game.pot.is_balanced(RoundName.TURN))
        self.assertTrue(turn.check_round_result() == [self.harry, self.tom])

    def test_turn_result_when_all_players_but_one_fold(self):
        # Given
        turn = Turn(players=self.flop.check_round_result(), deck=self.game.deck, pot=self.game.pot)

        # When
        self.harry.bet(self.game.pot, roundname=RoundName.TURN, to_putin=5)
        self.tom.fold()

        # Then
        self.assertTrue(self.phil.money == 149)
        self.assertTrue(self.harry.money == 293)
        self.assertTrue(self.tom.money == 48)
        self.assertTrue(self.anton.money == 1_000)
        self.assertTrue(self.game.pot.compute_total_sum() == 10)
        self.assertFalse(self.game.pot.is_balanced(RoundName.TURN))
        self.assertTrue(turn.check_round_result() == [self.harry])

    def test_turn_result_when_settled(self):
        # Given
        turn = Turn(players=self.flop.check_round_result(), deck=self.game.deck, pot=self.game.pot)

        # When
        self.harry.bet(self.game.pot, roundname=RoundName.FLOP, to_putin=5)
        self.tom.fold()
        turn.settle(turn.check_round_result())

        # Then
        self.assertTrue(self.phil.money == 149)
        self.assertTrue(self.harry.money == 303)
        self.assertTrue(self.tom.money == 48)
        self.assertTrue(self.anton.money == 1_000)
        self.assertTrue(self.game.pot.compute_total_sum() == 0)

    def test_turn_pot_is_balanced_when_one_is_all_in(self):
        # Given
        turn = Turn(players=self.flop.check_round_result(), deck=self.game.deck, pot=self.game.pot)
        # When
        self.harry.check()
        self.tom.bet(self.game.pot, RoundName.TURN, 9)
        self.harry.bet(self.game.pot, RoundName.TURN, 200)
        self.tom.call(self.game.pot, RoundName.TURN)

        # Then
        self.assertTrue(self.phil.money == 149)
        self.assertTrue(self.harry.money == 98)
        self.assertTrue(self.tom.money == 0)
        self.assertTrue(self.anton.money == 1_000)
        self.assertTrue(self.game.pot.compute_total_sum() == 253)
        self.assertTrue(self.game.pot.is_balanced(RoundName.TURN))
        self.assertTrue(turn.check_round_result() == [self.harry, self.tom])

    def test_run_turn(self):
        # Given
        turn = Turn(players=self.flop.check_round_result(), deck=self.game.deck, pot=self.game.pot)

        # When
        remaining_players = turn.run()

        # Then
        self.assertTrue(self.phil.money == 149)
        self.assertTrue(self.harry.money == 298)
        self.assertTrue(self.tom.money == 48)
        self.assertTrue(self.anton.money == 1_000)
        self.assertTrue(self.game.pot.is_balanced(RoundName.TURN))
        self.assertTrue(remaining_players == [self.harry, self.tom])
