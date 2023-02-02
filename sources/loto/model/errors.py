"""
Исключения.
"""


class RowArgsError(Exception):
    def __init__(self):
        super().__init__('number of Row constructor arguments must equal Row.tokens')


class CardArgsError(Exception):
    def __init__(self):
        super().__init__('number of Card constructor arguments must equal Card.rows')

