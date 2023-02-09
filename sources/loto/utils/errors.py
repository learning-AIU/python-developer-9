"""
Исключения.
"""

__all__ = [
    'CardError',
    'RowArgsError',
    'CardArgsError',
    'GameError',
    'GameInitError',
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
    message: str = 'use explicit Player instances or GameMode instance as Game constructor arguments'
    def __init__(self):
        super().__init__(self.message)
