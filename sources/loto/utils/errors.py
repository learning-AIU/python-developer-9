"""
Исключения.
"""

__all__ = [
    'RowArgsError',
    'CardArgsError',
]


class RowArgsError(Exception):
    message = 'number of Row constructor arguments must equal Row.tokens'
    def __init__(self):
        super().__init__(self.message)


class CardArgsError(Exception):
    message = 'number of Card constructor arguments must equal Card.rows'
    def __init__(self):
        super().__init__(self.message)

