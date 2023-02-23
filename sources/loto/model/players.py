"""
Участники игры.
"""

__all__ = [
    'Player',
    'Human',
    'Bot',
]

# импорт из модулей/пакетов стандартной библиотеки
from abc import ABC, abstractmethod
from random import choice

# импорт модулей/пакетов проекта
from loto import model
from loto import utils


class Player(ABC):
    """
    Абстрактный базовый класс, определяющий порядок реализации сущностей игроков.
    """
    number: int = 1

    def __init__(self, card: model.Card = None):
        self.name: str = ''
        if card is None:
            card = model.Card()
        self.card: model.Card = card
        self.fail: bool = False

    @abstractmethod
    def action(self, token: int, answer: utils.Answer) -> bool:
        """Запускает выполнение действия игроком во время его хода."""

    def _next(self, token: int) -> None:
        """Вызывается, если игрок не зачёркивает число на карточке."""
        if token in self.card:
            self.fail = True

    def _strike(self, token: int) -> None:
        """Вызывается, если игрок зачёркивает число на карточке."""
        if token in self.card:
            self.card.strike_token(token)
        else:
            self.fail = True


class Human(Player):
    """
    Реализация сущности игрока-человека.
    """
    def __init__(self, card: model.Card = None):
        super().__init__(card)
        self.name = f"{utils.INPUTS['human']} {self.number}".title()
        self.__class__.number += 1

    def action(self, token: int, answer: utils.Answer) -> bool:
        """Выполняет запрос к игроку-человеку о его выборе действия, выполняет выбранное действие и обрабатывает результат действия. Возвращает логическое значение, обозначающее завершение игры победой текущего игрока."""
        if answer is utils.Answer.NO:
            self._next(token)
            return False
        elif answer is utils.Answer.YES:
            self._strike(token)
            return bool(self.card)


class Bot(Player):
    """
    Реализация сущности игрока-бота.
    """
    def __init__(self,
                 card: model.Card = None,
                 *,
                 lvl: utils.DifficultyLvl = utils.DifficultyLvl.EASY):
        super().__init__(card)
        self.name = f"{utils.INPUTS['bot']} {self.number}".title()
        self.__class__.number += 1
        self.difficulty = lvl
        self._actions: list[bool] = [
            True
            for _ in range(int(self.difficulty*utils.SAMPLE_LENGTH))
        ] + [
            False
            for _ in range(int((1-self.difficulty)*utils.SAMPLE_LENGTH))
        ]
        self.last_action: utils.Answer = None

    def action(self, token: int, answer=None) -> bool:
        """Выполняет действие игрока-бота в зависимости от уровня сложности и обрабатывает результат действия. Возвращает логическое значение, обозначающее завершение игры победой текущего игрока."""
        ch = choice(self._actions)
        if token in self.card:
            action = (self._next, self._strike)[ch]
            self.last_action = (utils.Answer.NO, utils.Answer.YES)[ch]
        else:
            action = (self._strike, self._next)[ch]
            self.last_action = (utils.Answer.YES, utils.Answer.NO)[ch]
        action(token)
        return bool(self.card)

