import unittest

from games.Game import Game
from players.Player import ID_generator, Player


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
