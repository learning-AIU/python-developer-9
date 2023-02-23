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
        """Выводит в stdout надпись, выравнивая по центру окна терминала. Уровень влияет на регистр надписи и символ-заполнитель."""
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
        """Получает из stdin строки, обозначающие тип игроков (человек или бот), пока не получит пустую строку."""
        res = ''
        while True:
            prompt = (f"\n{utils.SYS_MARK}"
                      f"{utils.MESSAGES['get_player']}"
                      f"{utils.SYS_MARK}"
                      f"\n{utils.PROMPT}")
            inp = input(prompt)
            if inp:
                # формирует одну строку для последующей обработки представлением
                res += utils.SEP + inp.lower()
            else:
                return res.strip(utils.SEP)

    @staticmethod
    def get_turn() -> str:
        """Получает из stdin строку, ответ на вопрос о действии игрока."""
        prompt = (f"\n{utils.SYS_MARK}"
                  f"{utils.MESSAGES['action']}"
                  f"{utils.SYS_MARK}"
                  f"\n{utils.PROMPT}")
        return input(prompt).lower()

    def show_token(self, token: int):
        """Выводит в stdout номер очередного бочонка."""
        self.show_line(f'Бочонок: {token}', level=2)

    @staticmethod
    def show_card(player: model.Player):
        """Выводит в stdout карточку игрока."""
        print(f'\n{player.name:^{player.card.width}}')
        print(player.card)

    @staticmethod
    def show_bot_action(bot: model.Bot):
        """Выводит в stdout действие бота."""
        print(f'\n{utils.SYS_MARK}'
              f'{bot.name}'
              f'{utils.SYS_MARK}'
              f'\n{utils.PROMPT}'
              f'{utils.MESSAGES[bot.last_action.value]}')

    def show_winner(self, player: model.Player):
        """Выводит в stdout имя победителя."""
        self.show_line(f'{player.name} победил!', level=3)

    def show_tie(self):
        """Выводит в stdout сообщение о ничьей."""
        self.show_line('Ничья', level=3)

