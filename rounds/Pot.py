from typing import Dict

from players.Player import Player


class Pot:
    def __init__(self) -> None:
        self.preflop: Dict[Player, int] = {}

    def compute_total_sum(self) -> int:
        return sum(self.preflop.values())
