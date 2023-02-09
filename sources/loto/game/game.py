"""
Игровой процесс.
"""

__all__ = [
    'Game',
]

from random import choice, shuffle

from multimethod import multimeta

from loto import game
from loto import model
from loto import utils


# noinspection PyRedeclaration
class Game(metaclass=multimeta):
    """
    Содержит настройки для конкретной партии игры, список игроков и методы для реализации игрового процесса.
    """
    difficulty: utils.DifficultyLvl = utils.DifficultyLvl.EASY
    players_number: int = 2

    def __init__(self,
                 player1: game.Player,
                 player2: game.Player,
                 *players: game.Player):
        self.players = list((player1, player2) + players)
        players_set = {type(pl) for pl in self.players}
        if players_set == {game.Human}:
            self.mode: utils.GameMode = utils.GameMode.PVP
        elif players_set == {game.Human, game.Bot}:
            self.mode: utils.GameMode = utils.GameMode.PVB
        elif players_set == {game.Bot}:
            self.mode: utils.GameMode = utils.GameMode.BVB
        else:
            raise utils.GameInitError
        self.__post_init__()

    def __init__(self, mode: utils.GameMode):
        self.players: list[game.Player]
        if mode is utils.GameMode.PVP:
            self.players = [game.Human()
                            for _ in range(self.players_number)]
        elif mode is utils.GameMode.PVB:
            q = [game.Human(), game.Bot(lvl=self.difficulty)]
            self.players = q + [choice(q)
                                for _ in range(self.players_number-2)]
        elif mode is utils.GameMode.BVB:
            self.players = [game.Bot(lvl=self.difficulty)
                            for _ in range(self.players_number)]
        else:
            raise utils.GameInitError
        self.mode = mode
        self.__post_init__()

    def __post_init__(self):
        tokens = [model.Token(i)
                  for i in range(model.Token.minimum, model.Token.maximum+1)]
        shuffle(tokens)
        self._purse: set[model.Token] = set(tokens)

    @property
    def get_token(self) -> model.Token:
        return self._purse.pop()

    def check_fail(self) -> None:
        for player in iter(self.players):
            if player.fail:
                self.players.remove(player)

