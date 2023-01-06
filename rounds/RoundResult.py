from players.Player import Player
from rounds.RoundName import RoundName


class RoundResult:
    def __init__(self, is_game_ended: bool, roundname: RoundName, winner: Player) -> None:
        self.is_game_ended = is_game_ended
        self.roundname = roundname
        self.winner = winner
