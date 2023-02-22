"""
Глобальные переменные и константы.
"""

__all__ = [
    'GameMode',
    'DifficultyLvl',
    'Answer',
    'SAMPLE_LENGTH',
    'APP_TITLE',
    'FILLER_1',
    'FILLER_2',
    'FILLER_3',
    'SYS_MARK',
    'MESSAGES',
    'PROMPT',
    'INPUTS',
    'SEP',
    'pat_human',
    'pat_bot_easy',
    'pat_bot_hard',
]

# импорт из модулей/пакетов стандартной библиотеки
from decimal import Decimal as dec
from enum import Enum
from re import compile


class GameMode(Enum):
    PVP = 'player versus player'
    PVB = 'player versus bot'
    BVB = 'bot versus bot'


class DifficultyLvl(dec, Enum):
    EASY = dec('0.97')
    HARD = dec('1.0')


class Answer(Enum):
    YES = 'yд1'
    NO = 'nн0'


SAMPLE_LENGTH = 1000


APP_TITLE = 'ЛОТО'
FILLER_1 = '='
FILLER_2 = '+'
FILLER_3 = '_'

SYS_MARK = ' _ '
MESSAGES = {
    'get_player': 'введите Игрок или Бот Лёгкий или Бот Сложный или пустую строку',
    'action': 'зачеркнуть? [д/н]',
    'new_game': 'Новая игра',
    Answer.NO.value: 'продолжить',
    Answer.YES.value: 'зачеркнуть',
    '': '',
}

PROMPT = ' > '
INPUTS = {
    'human': 'игрок',
    'bot': 'бот',
    'easy': 'легкий',
    'hard': 'сложный',
    '': '',
}

SEP = '_'

pat_human = compile(
    rf"{INPUTS['human'][0]}|{INPUTS['human']}"
)
pat_bot_easy = compile(
    rf"(?:{INPUTS['bot'][0]}|{INPUTS['bot']}) ?"
    rf"(?:{INPUTS['easy'][0]}|{INPUTS['easy']})"
)
pat_bot_hard = compile(
    rf"(?:{INPUTS['bot'][0]}|{INPUTS['bot']}) ?"
    rf"(?:{INPUTS['hard'][0]}|{INPUTS['hard']})"
)

