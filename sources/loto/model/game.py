"""
Игровой процесс.
"""

__all__ = [
    'Game',
]

# импорт из модулей/пакетов стандартной библиотеки
from multimethod import multimeta
from random import choice, shuffle

# импорт модулей/пакетов проекта
from . import players
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
                 player1: players.Player,
                 player2: players.Player,
                 *players_: players.Player):
        self.players = list((player1, player2) + players_)
        players_set = {type(pl) for pl in self.players}
        if players_set == {players.Human}:
            self.mode: utils.GameMode = utils.GameMode.PVP
        elif players_set == {players.Human, players.Bot}:
            self.mode: utils.GameMode = utils.GameMode.PVB
        elif players_set == {players.Bot}:
            self.mode: utils.GameMode = utils.GameMode.BVB
        else:
            raise utils.GameInitError
        self.__post_init__()

    def __init__(self, mode: utils.GameMode):
        self.players: list[players.Player]
        if mode is utils.GameMode.PVP:
            self.players = [players.Human()
                            for _ in range(self.players_number)]
        elif mode is utils.GameMode.PVB:
            q = [players.Human(), players.Bot(lvl=self.difficulty)]
            self.players = q + [choice(q)
                                for _ in range(self.players_number-2)]
        elif mode is utils.GameMode.BVB:
            self.players = [players.Bot(lvl=self.difficulty)
                            for _ in range(self.players_number)]
        else:
            raise utils.GameInitError
        self.mode = mode
        self.__post_init__()

    def __post_init__(self):
        tokens = [model.Token(i)
                  for i in range(model.Token.minimum, model.Token.maximum+1)]
        shuffle(tokens)
        self._purse: list[model.Token] = tokens

    @property
    def get_token(self) -> model.Token | None:
        try:
            t = self._purse.pop()
        except IndexError:
            return None
        else:
            return t

    def check_fail(self) -> int:
        self.players = [pl for pl in self.players if not pl.fail]
        return len(self.players)

