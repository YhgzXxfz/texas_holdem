from typing import Tuple

from games.Deck import Deck
from players.Player import Player
from rounds.Pot import Pot


class Round:
    def __init__(self, players: Tuple[Player], deck: Deck) -> None:
        self.deck = deck
        self.players = players

    def run() -> None:
        pass


class Preflop(Round):
    def __init__(
        self, players: Tuple[Player, ...], deck: Deck, pot: Pot, small_blind: int = 1, big_blind: int = 2
    ) -> None:
        super().__init__(players, deck)
        self._build_pot(pot, small_blind, big_blind)
        self._distribute_hands()

    def _build_pot(self, pot: Pot, small_blind: int, big_blind: int) -> None:
        pot.preflop[self.players[0]] = small_blind
        pot.preflop[self.players[1]] = big_blind

    def _distribute_hands(self) -> None:
        n = len(self.players)
        hands = list(self.deck.pop_cards(2 * n))
        for (p, h) in zip(self.players, zip(hands[0:n], hands[n:])):
            p.hands = h

    def run() -> None:
        pass
