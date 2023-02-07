"""
Исключения.
"""

__all__ = [
    'RowArgsError',
    'CardArgsError',
]


class CardError(Exception):
    message: str
    def __init__(self):
        super().__init__(self.message)


class RowArgsError(CardError):
    message = 'number of Row constructor arguments must equal Row.tokens'


class CardArgsError(CardError):
    message = 'number of Card constructor arguments must equal Card.rows'


class GameError(Exception):
    pass


class GameInitError(GameError):
    pass
