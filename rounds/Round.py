from functools import reduce
from typing import List, Tuple

from cards.Card import Card
from games.Deck import Deck
from players.Player import Player
from rounds.Pot import Pot
from rounds.RoundName import RoundName
from rounds.RoundResult import RoundResult


class Round:
    def __init__(self, players: Tuple[Player], deck: Deck, pot: Pot) -> None:
        self.deck = deck
        self.players = players
        self.pot = pot
        self._get_ready_for_players()

    def get_starting_index(self) -> int:
        raise NotImplementedError

    def get_round_name(self) -> RoundName:
        raise NotImplementedError

    def settle(self, remaining_players: List[Player]) -> RoundResult:
        raise NotImplementedError

    def check_round_result(self) -> List[Player]:
        players = [p for p in self.players if p.is_in_game]
        if len(players) == 1:
            return players

        if self._all_players_have_taken_action(players) and self.pot.is_balanced(self.get_round_name()):
            return players

        return []

    def run(self) -> List[Player]:
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

    def _get_ready_for_players(self) -> None:
        for p in self.players:
            p.has_taken_action = False

    def _provide_shared_hands(self) -> Tuple[Card]:
        raise NotImplementedError


class Preflop(Round):
    def __init__(
        self, players: Tuple[Player, ...], deck: Deck, pot: Pot, small_blind: int = 1, big_blind: int = 2
    ) -> None:
        super().__init__(players, deck, pot)
        self._build_pot(small_blind, big_blind)
        self._distribute_hands()

    def _build_pot(self, small_blind: int, big_blind: int) -> None:
        self.pot.initialize_round(roundname=RoundName.PREFLOP, players=self.players)
        self.players[0].bet_bind(self.pot, small_blind)
        self.players[1].bet_bind(self.pot, big_blind)

    def _distribute_hands(self) -> None:
        n = len(self.players)
        cards = list(self.deck.pop_cards(2 * n))
        for (p, h) in zip(self.players, zip(cards[0:n], cards[n:])):
            p.pocket_cards = h

    def get_starting_index(self) -> int:
        return 2

    def get_round_name(self) -> RoundName:
        return RoundName.PREFLOP

    def settle(self, remaining_players: List[Player]) -> RoundResult:
        if len(remaining_players) == 1:
            self.pot.settle(remaining_players[0])
            return RoundResult(True, self.get_round_name(), remaining_players[0])
        else:
            return RoundResult(False, self.get_round_name(), None)


class Flop(Round):
    def __init__(self, players: Tuple[Player, ...], deck: Deck, pot: Pot) -> None:
        super().__init__(players, deck, pot)
        self.community_cards = self._provide_community_hands()
        self.pot.initialize_round(roundname=RoundName.FLOP, players=self.players)

    def get_starting_index(self) -> int:
        return 0

    def get_round_name(self) -> RoundName:
        return RoundName.FLOP

    def settle(self, remaining_players: List[Player]) -> RoundResult:
        if len(remaining_players) == 1:
            self.pot.settle(remaining_players[0])
            return RoundResult(True, self.get_round_name(), remaining_players[0])
        else:
            return RoundResult(False, self.get_round_name(), None)

    def _provide_community_hands(self) -> Tuple[Card]:
        self.deck.skip_one_card()
        return self.deck.pop_cards(3)


class Turn(Round):
    def __init__(self, players: Tuple[Player, ...], deck: Deck, pot: Pot) -> None:
        super().__init__(players, deck, pot)
        self.community_cards = self._provide_community_hands()
        self.pot.initialize_round(roundname=RoundName.TURN, players=self.players)

    def get_starting_index(self) -> int:
        return 0

    def get_round_name(self) -> RoundName:
        return RoundName.TURN

    def settle(self, remaining_players: List[Player]) -> RoundResult:
        if len(remaining_players) == 1:
            self.pot.settle(remaining_players[0])
            return RoundResult(True, self.get_round_name(), remaining_players[0])
        else:
            return RoundResult(False, self.get_round_name(), None)

    def _provide_community_hands(self) -> Tuple[Card]:
        self.deck.skip_one_card()
        return self.deck.pop_cards(1)


class River(Round):
    def __init__(self, players: Tuple[Player, ...], deck: Deck, pot: Pot) -> None:
        super().__init__(players, deck, pot)
        self.community_cards = self._provide_community_hands()
        self.pot.initialize_round(roundname=RoundName.RIVER, players=self.players)

    def get_starting_index(self) -> int:
        return 0

    def get_round_name(self) -> RoundName:
        return RoundName.RIVER

    def settle(self, remaining_players: List[Player]) -> RoundResult:
        if len(remaining_players) == 1:
            self.pot.settle(remaining_players[0])
            return RoundResult(True, self.get_round_name(), remaining_players[0])
        else:
            return RoundResult(False, self.get_round_name(), None)

    def _provide_community_hands(self) -> Tuple[Card]:
        self.deck.skip_one_card()
        return self.deck.pop_cards(1)
