from collections import OrderedDict
from functools import reduce
from typing import List, OrderedDict

from cards.Card import Card
from evaluations.EvaluatorOf5Cards import EvaluatorOf5Cards
from evaluations.EvaluatorOf7Cards import EvaluatorOf7Cards
from games.Deck import Deck
from rounds.Pot import Pot
from rounds.Round import Flop, Preflop, River, Turn


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
        return [ply for (_pos, ply) in sorted(self.player_list.items()) if ply.is_in_game is True]

    def start(self) -> None:
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
            return

        # 2. Flop
        #    2.1 flop cards
        #    2.2 bet round
        flop = Flop(
            players=remaining_players,
            deck=self.deck,
            pot=self.pot,
        )
        remaining_players = flop.run()
        round_result = flop.settle(remaining_players)
        if round_result.is_game_ended:
            return

        # 3. Turn
        #    3.1 turn card
        #    3.2 bet round
        turn = Turn(
            players=remaining_players,
            deck=self.deck,
            pot=self.pot,
        )
        remaining_players = turn.run()
        round_result = turn.settle(remaining_players)
        if round_result.is_game_ended:
            return

        # 4. River
        #    4.1 river hand
        #    4.2 bet round
        river = River(
            players=remaining_players,
            deck=self.deck,
            pot=self.pot,
        )
        remaining_players = river.run()
        round_result = river.settle(remaining_players)
        if round_result.is_game_ended:
            return

        # Showdown
        eva_to_players = self.showdown(
            reduce(
                lambda acc, it: acc + it,
                map(list, (flop.community_cards, turn.community_cards, river.community_cards)),
                [],
            ),
            remaining_players,
        )
        self.settle_showdown(eva_to_players)

    def showdown(self, community_cards: List[Card], remaining_players: List) -> OrderedDict[EvaluatorOf5Cards, List]:
        result: OrderedDict[EvaluatorOf5Cards, List] = OrderedDict()
        player_to_evaluation = [
            (player, EvaluatorOf7Cards(community_cards + list(player.pocket_cards)).getOptimalHands())
            for player in remaining_players
        ]
        for player, eva in player_to_evaluation:
            if eva in result:
                result[eva].append(player)
            else:
                result[eva] = [player]

        result = {eva: sorted(players, key=lambda p: self.pot.get_chips_for(p)) for eva, players in result.items()}
        result = OrderedDict(sorted(result.items(), key=lambda pair: pair[0], reverse=True))
        return result

    def settle_showdown(self, evaluation_to_players: OrderedDict[EvaluatorOf5Cards, List]) -> int:
        remaining_players = set(self.player_list.values())

        pot_at_showdown = {player: self.pot.get_chips_for(player) for _pos, player in self.player_list.items()}

        # In case there is remainder
        surplus = 0

        # iteration is just for the algorithm efficiency testing purpose
        iteration = 0
        while len(evaluation_to_players) > 0:
            eva = next(iter(evaluation_to_players))
            players = evaluation_to_players.pop(eva)

            remaining_players = remaining_players.difference(players)
            pot_of_weaker_hands = {
                player: chip for player, chip in pot_at_showdown.items() if player in remaining_players
            }

            while len(players) > 0:
                curr = players[0]
                bet = pot_at_showdown[curr]

                if bet == 0:
                    # remove curr player and jump to the next
                    players.pop(0)
                    continue

                if sum(pot_at_showdown.values()) == 0:
                    break

                iteration += 1
                # Each player from this current tier gets back from self
                # Ensured for the pot to have sufficient remainings as the player list is sorted by betting chips
                for peer in players:
                    peer.money += bet
                    pot_at_showdown[peer] -= bet

                # All players from this current tier get from people with weaker hands
                # The chips from people with weaker hands will be split equally
                total_owe = sum(min(chip, bet) for _other, chip in pot_of_weaker_hands.items())
                n = len(players)
                owe, remainder = total_owe // n, total_owe % n
                surplus += remainder

                # Distribute
                for peer in players:
                    peer.money += owe

                # Update chips in the pot for people with weaker hands
                pot_of_weaker_hands = {other: max(0, chip - bet) for other, chip in pot_of_weaker_hands.items()}
                pot_at_showdown = {
                    p: pot_at_showdown[p] for p in set(pot_at_showdown) - set(pot_of_weaker_hands)
                } | pot_of_weaker_hands

                players.pop(0)

        # All remainder goes to the first person to the left of the dealer
        self.get_players_in_the_game()[0].money += surplus
        return iteration
