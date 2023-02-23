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
        # из этого списка флагов бот в дальнейшем будет выбирать один для верного/неверного действия — пропорция количества элементов True и False определяется значениями элементов перечислителя DifficultyLvl и означает вероятность ошибки бота
        self._actions: list[bool] = [
            True
            for _ in range(int(lvl*utils.SAMPLE_LENGTH))
        ] + [
            # для высокого уровня сложности эта часть списка должна быть пустой — таким образом сложный бот никогда не будет ошибаться
            False
            for _ in range(int((1-lvl)*utils.SAMPLE_LENGTH))
        ]
        self.last_action: utils.Answer | None = None

    def action(self, token: int, answer=None) -> bool:
        """Выполняет действие игрока-бота в зависимости от уровня сложности и обрабатывает результат действия. Возвращает логическое значение, обозначающее завершение игры победой текущего игрока."""
        ch = choice(self._actions)
        if token in self.card:
            # верное действие
            if ch:
                action = self._strike
                self.last_action = utils.Answer.YES
            # неверное действие
            else:
                action = self._next
                self.last_action = utils.Answer.NO
        else:
            # верное действие
            if ch:
                action = self._next
                self.last_action = utils.Answer.NO
            # неверное действие
            else:
                action = self._strike
                self.last_action = utils.Answer.YES
        action(token)
        return bool(self.card)

