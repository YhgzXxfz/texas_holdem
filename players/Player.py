import random
import string
from enum import Enum

import rounds.RoundName as rn
from players.Policy import Policy


def ID_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return "".join(random.SystemRandom().choice(chars) for _ in range(size))


class ActionType(Enum):
    CHECK = "check"
    FOLD = "fold"
    BET = "bet"
    RAISE = "raise"
    CALL = "call"


class Player:
    def __init__(self, name: str, ID: str, money: int, policy: Policy = Policy.ALWAYS_CHECK_OR_FOLD):
        self.name = name
        self.money = money
        self.ID = ID
        self.hands = ()
        self.is_in_game = False
        self.has_taken_action = False
        self.policy = policy

    def join_game(self, game, position: int) -> None:
        game.add_player(self, position)
        self.is_in_game = True

    def take_from_pot(self, pot) -> None:
        self.money += pot.compute_total_sum()

    def take_action(self, pot, roundname: rn.RoundName) -> None:
        if self.policy == Policy.ALWAYS_CHECK_OR_FOLD:
            if pot.is_balanced(roundname):
                self.check()
            else:
                self.fold()
        else:
            if pot.is_balanced(roundname):
                self.check()
            else:
                self.call(pot, roundname)

    def call(self, pot, roundname: rn.RoundName) -> None:
        to_putin = max(pot.roundpots[roundname].values()) - pot.roundpots[roundname][self]
        self._add_to_pot(pot, roundname, to_putin)
        self.has_taken_action = True

    def fold(self) -> None:
        self.is_in_game = False
        self.has_taken_action = True

    def bet(self, pot, roundname: rn.RoundName, to_putin: int) -> None:
        self._add_to_pot(pot, roundname, to_putin)
        self.has_taken_action = True

    def _add_to_pot(self, pot, roundname: rn.RoundName, to_putin: int) -> None:
        to_putin = min(to_putin, self.money)
        self.money -= to_putin
        pot.add(self, roundname, to_putin)

    def check(self) -> None:
        self.has_taken_action = True

    def __eq__(self, o: object) -> bool:
        return self.ID == o.ID

    def __hash__(self) -> int:
        return hash(self.ID)
