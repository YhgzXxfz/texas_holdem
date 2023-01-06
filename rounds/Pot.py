from typing import Dict, List

import players.Player as ply
import rounds.RoundName as rn


class Pot:
    def __init__(self) -> None:
        self.roundpots: Dict[rn.RoundName, Dict[ply.Player, int]] = {}

    def compute_total_sum(self) -> int:
        return sum(chip for roundpot in self.roundpots.values() for chip in roundpot.values())

    def _compute_round_pot_sum(self, roundname: rn.RoundName) -> int:
        return sum(self.roundpots[roundname].values())

    def initialize_round(self, roundname: rn.RoundName, players: List[ply.Player]) -> None:
        self.roundpots[roundname] = {p: 0 for p in players}

    def is_balanced(self, roundname: rn.RoundName) -> bool:
        return self._is_balanced(self.roundpots[roundname])

    def add(self, player: ply.Player, roundname: rn.RoundName, to_putin: int) -> None:
        self.roundpots[roundname][player] += to_putin

    def settle(self, winner: ply.Player) -> None:
        winner.take_from_pot(self)
        self._clear()

    def _is_balanced(self, roundpot: Dict[ply.Player, int]) -> bool:
        count, chip = 0, max(roundpot.values())
        for (p, m) in roundpot.items():
            if not p.is_in_game:
                continue
            if chip != m and p.money > 0:
                return False
            else:
                count += 1

        return count > 1

    def _clear(self) -> None:
        self.roundpots.clear()
