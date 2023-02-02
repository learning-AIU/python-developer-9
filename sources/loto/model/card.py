"""
Игровые элементы.
"""

from random import randint, randrange
from typing import Self


class Token(int):
    """
    Бочонок лото генерируется как случайное число в заданном диапазоне включая границы. При передаче в конструктор аргумента, выходящего за границы диапазона, объект принимает значение ближайшей границы.
    """
    minimum: int = 1
    maximum: int = 90
    width: int = len(str(maximum))

    def __new__(cls, number: int = None) -> Self:
        if number is None:
            return super().__new__(cls, randint(cls.minimum, cls.maximum))
        else:
            if number < cls.minimum:
                return super().__new__(cls, cls.minimum)
            elif number > cls.maximum:
                return super().__new__(cls, cls.maximum)
            else:
                return super().__new__(cls, number)

    def __init__(self, number: int = None):
        self.strike: bool = False

    def __str__(self):
        if self.strike:
            return '-'*self.width
        else:
            return f'{self:>{self.width}}'


class Row(tuple):
    """
    Строка карточки конструируется как кортеж экземпляров Token и None на основании переданных в конструктор чисел. Количество аргументов конструктора должно быть равно атрибуту _tokens.
    """
    cells: int = 9
    tokens: int = 5

    def __new__(cls, *args: int | Token) -> Self:
        if len(args) != cls.tokens:
            raise ValueError('number of Row constructor arguments must equal Row.tokens')
        else:
            tokens: list[Token | None] = sorted(Token(n) for n in args)
            for i in range(1, cls.cells - cls.tokens + 1):
                tokens.insert(randrange(cls.tokens + i), None)
            return super().__new__(cls, tokens)

    def __str__(self):
        return ' '.join(
            ' '*Token.width if elem is None else str(elem)
            for elem in self
        )

