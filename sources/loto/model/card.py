"""
Игровые элементы.
"""

from random import randint
from typing import Self


class Token(int):
    """
    Бочонок лото генерируется как случайное число в заданном диапазоне включая границы. При передаче в конструктор аргумента, выходящего за границы диапазона, объект принимает значение ближайшей границы.
    """
    _minimum: int = 1
    _maximum: int = 90

    def __new__(cls, number: int = None) -> Self:
        if number is None:
            return super().__new__(cls, randint(cls._minimum, cls._maximum))
        else:
            if number < cls._minimum:
                return super().__new__(cls, cls._minimum)
            elif number > cls._maximum:
                return super().__new__(cls, cls._maximum)
            else:
                return super().__new__(cls, number)

    def __init__(self, number: int = None):
        self.strike: bool = False

    def __str__(self):
        width = len(str(self._maximum))
        if self.strike:
            return '-'*width
        else:
            return f'{self:>{width}}'

