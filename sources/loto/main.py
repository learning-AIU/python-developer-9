"""
Игра Лото.
"""

# импорт модулей/пакетов проекта
from loto import cli
from loto import controller
from loto import utils


def main():
    """Инициализирует и запускает игру."""
    app = controller.Controller(cli.View())
    app.view.show_line(utils.APP_TITLE)
    while True:
        # новая партия
        app.view.show_line(utils.MESSAGES['new_game'], level=3)
        app.set_game()
        app.start_game()


if __name__ == '__main__':
    # точка входа
    main()
