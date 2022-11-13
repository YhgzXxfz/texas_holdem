import random
import string

import games


def ID_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return "".join(random.SystemRandom().choice(chars) for _ in range(size))


class Player:
    def __init__(self, name: str, ID: str, money: int):
        self.name = name
        self.money = money
        self.ID = ID
        self.hands = ()
        self.is_in_game = False

    def join_game(self, game, position: int):
        game.add_player(self, position)
        self.is_in_game = True

    def __eq__(self, o: object) -> bool:
        return self.ID == o.ID
