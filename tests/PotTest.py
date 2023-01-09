import unittest

from games.Game import Game
from players.Player import ID_generator, Player
from players.Policy import Policy
from rounds.Pot import Pot
from rounds.RoundName import RoundName


class PotTest(unittest.TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def test_chips_are_calculated_for_each_player(self) -> None:
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

        # When
        pot = Pot()
        pot.roundpots = {
            RoundName.PREFLOP: {phil: 10, harry: 10, tom: 10, anton: 10},
            RoundName.FLOP: {phil: 10, harry: 10, tom: 10, anton: 10},
            RoundName.TURN: {phil: 0, harry: 0, tom: 0, anton: 0},
            RoundName.RIVER: {phil: 50, harry: 50, tom: 30, anton: 50},
        }

        # Then
        self.assertTrue(pot.get_chips_for(phil) == 70)
        self.assertTrue(pot.get_chips_for(harry) == 70)
        self.assertTrue(pot.get_chips_for(tom) == 50)
        self.assertTrue(pot.get_chips_for(anton) == 70)
