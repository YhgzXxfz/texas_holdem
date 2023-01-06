from players.Player import Player


class RoundResult:
    def __init__(self, is_game_ended: bool, winner: Player) -> None:
        self.is_game_ended = is_game_ended
        self.winner = winner
