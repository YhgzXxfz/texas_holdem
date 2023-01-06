from typing import List

from games.Deck import Deck
from rounds.Pot import Pot
from rounds.Round import Preflop


class Game:
    def __init__(self, small_blind=1, big_blind=2):
        self.player_list = {}
        self.small_blind = small_blind
        self.big_blind = big_blind
        self.pot = Pot()
        self.deck = Deck()

    def add_player(self, player, position: int) -> None:
        if self.player_list.get(position) is not None:
            raise KeyError

        self.player_list[position] = player

    def get_players_in_the_game(self) -> List:
        return [ply for (_pos, ply) in sorted(self.player_list.items())]

    def start(self) -> str:
        # 1. Preflop
        #    1.1 distribute cards to players
        #    1.2 SB, BB
        #    1.3 bet round
        preflop = Preflop(
            players=self.get_players_in_the_game(),
            deck=self.deck,
            pot=self.pot,
            small_blind=self.small_blind,
            big_blind=self.big_blind,
        )
        remaining_players = preflop.run()
        round_result = preflop.settle(remaining_players)
        if round_result.is_game_ended:
            msg = f"Game ends in preflop. Winner is {round_result.winner.name}!"
            return msg
        else:
            return "Game is not ended at preflop"

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
