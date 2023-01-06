from typing import List


class Game:
    def __init__(self):
        self.player_list = {}

    def add_player(self, player, position: int) -> None:
        if self.player_list.get(position) is not None:
            raise KeyError

        self.player_list[position] = player

    def get_players_in_the_game(self) -> List:
        return [ply for (_pos, ply) in sorted(self.player_list.items())]

    def start():
        # 1. Preflop
        #    1.1 distribute cards to players
        #    1.2 SB, BB
        #    1.3 bet round
        # 2. Flop
        #    2.1 flop cards
        #    2.2 bet round
        # 3. Turn
        #    3.1 turn card
        #    3.2 bet round
        # 4. River
        #    4.1 river hand
        #    4.2 bet round
        # 5. Comparison
        pass
