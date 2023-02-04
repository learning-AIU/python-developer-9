"""
Игровые элементы.
"""

__all__ = [
    'Token',
    'Card',
]

# импорт из модулей/пакетов стандартной библиотеки
from collections.abc import Iterable
from random import randint, randrange, shuffle
from typing import Self

# импорт модулей/пакетов проекта
from loto import utils


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

    def __new__(cls, *args: int) -> Self:
        if len(args) != cls.tokens:
            raise utils.RowArgsError
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


class Card(list):
    """
    Карточка состоит из сгенерированных экземпляров Row. В конструктор Row передаётся необходимое количество уникальных экземпляров Token.
    """
    rows: int = 3
    cells: int = Row.cells * rows
    tokens: int = Row.tokens * rows

    def __init__(self, *args: Iterable[int]):
        super().__init__()
        numbers = list(range(Token.minimum, Token.maximum + 1))
        shuffle(numbers)
        if args:
            if len(args) != self.rows:
                raise utils.CardArgsError
            rows = [Row(*arg) for arg in args]
        else:
            rows = [
                Row(*[
                    numbers.pop()
                    for _ in range(Row.tokens)
                ])
                for _ in range(self.rows)
            ]
        for row in rows:
            self.append(row)
        self.width = Row.cells*(Token.width + 1) - 1

    def __getitem__(self, index: int) -> Token | None:
        if isinstance(index, int):
            i, j = divmod(index, Row.cells)
            return super().__getitem__(i)[j]
        else:
            raise TypeError(f'Card indices must be integers, not {index.__class__.__name__}')

    def __str__(self):
        h_line = '-'*self.width
        return '\n'.join([
            h_line,
            *(str(r) for r in self),
            h_line
        ])

    def strike_token(self, token: Token) -> None:
        """"""
        i = [t for r in self for t in r].index(token)
        card_token = self[i]
        if card_token is not None:
            card_token.strike = True

