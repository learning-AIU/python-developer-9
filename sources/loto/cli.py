"""
Представление для интерфейса командной строки.
"""

# импорт из модулей/пакетов стандартной библиотеки
from shutil import get_terminal_size
from typing import Literal

# импорт модулей/пакетов проекта
from loto import model
from loto import utils


class View:
    """
    Ввод и вывод данных в интерфейсе командной строки.
    """
    terminal_width = get_terminal_size()[0] - 1

    def show_line(self, text: str, level: Literal[1, 2, 3] = 1):
        if level == 1:
            text = text.upper()
        elif level == 2:
            text = text.title()
        elif level == 3:
            text = text.capitalize()
        filler = getattr(utils, f'FILLER_{level}')
        line = f" {text} ".center(self.terminal_width-2, filler)
        print(f'\n {line} ')

    @staticmethod
    def get_players() -> str:
        res = ''
        while True:
            prompt = (f"\n{utils.SYS_MARK}"
                      f"{utils.MESSAGES['get_player']}"
                      f"{utils.SYS_MARK}"
                      f"\n{utils.PROMPT}")
            inp = input(prompt)
            if inp:
                res += utils.SEP + inp.lower()
            else:
                return res.strip(utils.SEP)

    @staticmethod
    def get_turn() -> str:
        prompt = (f"\n{utils.SYS_MARK}"
                  f"{utils.MESSAGES['action']}"
                  f"{utils.SYS_MARK}"
                  f"\n{utils.PROMPT}")
        return input(prompt).lower()

    def show_token(self, token: int):
        self.show_line(f'Бочонок: {token}', level=2)

    @staticmethod
    def show_card(player: model.Player):
        print(f'\n{player.name:^{player.card.width}}')
        print(player.card)

    @staticmethod
    def show_bot_action(bot: model.Bot):
        print(f'\n{utils.SYS_MARK}'
              f'{bot.name}'
              f'{utils.SYS_MARK}'
              f'\n{utils.PROMPT}'
              f'{utils.MESSAGES[bot.last_action.value]}')

    def show_winner(self, player: model.Player):
        self.show_line(f'{player.name} победил!', level=3)

    def show_tie(self):
        self.show_line('Ничья', level=3)

