import players


class Game:
    def __init__(self):
        self.player_list = []

    def add_player(self, player, position: int):
        self.player_list.insert(position, player)

    def start():
        # 1. Preflop
        #    1.1 distribute cards to players
        #    1.2 SB, BB
        #    1.3 bet round
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
        pass
