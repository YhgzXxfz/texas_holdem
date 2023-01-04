from functools import reduce
from typing import List, Tuple

from games.Deck import Deck
from players.Player import ActionType, Player
from rounds.Pot import Pot
from rounds.RoundName import RoundName


class Round:
    def __init__(self, players: Tuple[Player], deck: Deck, pot: Pot) -> None:
        self.deck = deck
        self.players = players
        self.pot = pot
        for p in self.players:
            p.has_taken_action = False

    def get_starting_index(self) -> int:
        raise NotImplementedError

    def get_round_name(self) -> RoundName:
        raise NotImplementedError

    def check_round_result(self) -> List[Player]:
        players = [p for p in self.players if p.is_in_game]
        if len(players) == 1:
            return players

        if self._all_players_have_taken_action(players) and self.pot.is_balanced(self.get_round_name()):
            return players

        return []

    def run(self) -> None:
        index = self.get_starting_index()
        while True:
            players = [p for p in self.players if p.is_in_game]
            if len(players) == 1:
                return players

            if self._all_players_have_taken_action(players) and self.pot.is_balanced(self.get_round_name()):
                return players

            index = index % len(players)
            players[index].take_action(self.pot, self.get_round_name())
            index += 1

    def _all_players_have_taken_action(self, players: List[Player]) -> bool:
        return reduce(lambda result, p: result and p.has_taken_action, players, True)


class Preflop(Round):
    def __init__(
        self, players: Tuple[Player, ...], deck: Deck, pot: Pot, small_blind: int = 1, big_blind: int = 2
    ) -> None:
        super().__init__(players, deck, pot)
        self._build_pot(small_blind, big_blind)
        self._distribute_hands()

    def _build_pot(self, small_blind: int, big_blind: int) -> None:
        self.pot.initialize_round(roundname=RoundName.PREFLOP, players=self.players)
        self.players[0].bet(self.pot, self.get_round_name(), small_blind)
        self.players[1].bet(self.pot, self.get_round_name(), big_blind)

    def _distribute_hands(self) -> None:
        n = len(self.players)
        hands = list(self.deck.pop_cards(2 * n))
        for (p, h) in zip(self.players, zip(hands[0:n], hands[n:])):
            p.hands = h

    def get_starting_index(self) -> int:
        return 2

    def get_round_name(self) -> RoundName:
        return RoundName.PREFLOP
