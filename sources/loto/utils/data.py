"""
Глобальные переменные и константы.
"""

__all__ = [
    'GameMode',
    'SAMPLE_LENGTH',
    'DifficultyLvl',
    'Answer',
]

# импорт из модулей/пакетов стандартной библиотеки
from decimal import Decimal as dec
from enum import Enum


class GameMode(Enum):
    PVP = 'player versus player'
    PVB = 'player versus bot'
    BVB = 'bot versus bot'


class DifficultyLvl(dec, Enum):
    EASY = dec('0.9')
    HARD = dec('1.0')


SAMPLE_LENGTH = 1000


class Answer(Enum):
    YES = 'y'
    NO = 'n'

