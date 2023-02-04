"""
Участники игры.
"""

from abc import ABC, abstractmethod

from loto import main
from loto import model
from loto import utils


class Player(ABC):
    """
    Абстрактный базовый класс, определяющий порядок реализации сущностей игроков.
    """
    def __init__(self, card: model.Card = None):
        if card is None:
            card = model.Card()
        self.card: model.Card = card
        self.fail: bool = False

    @abstractmethod
    def action(self, token: int) -> bool:
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
    def action(self, token: int) -> bool:
        """Выполняет запрос к игроку-человеку о его выборе действия, выполняет выбранное действие и обрабатывает результат действия. Возвращает логическое значение, обозначающее завершение игры победой текущего игрока."""
        ans = main.Controller.get_input()
        if ans is utils.Answer.NO:
            self._next(token)
            return False
        elif ans is utils.Answer.YES:
            self._strike(token)
            return bool(self.card)


class Bot(Player):
    """

    """

