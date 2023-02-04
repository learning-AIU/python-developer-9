"""
Глобальные переменные и константы.
"""

__all__ = [
    'GameMode',
    'DifficultyLvl',
    'Answer',
]

# импорт из модулей/пакетов стандартной библиотеки
from enum import Enum


class GameMode(Enum):
    PVP = 'player versus player'
    PVB = 'player versus bot'
    BVB = 'bot versus bot'


class DifficultyLvl(Enum):
    EASY = 1
    HARD = 2


class Answer(Enum):
    YES = 'y'
    NO = 'n'

