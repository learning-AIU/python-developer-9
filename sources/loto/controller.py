"""
Управление процессом игры.
"""

# импорт модулей/пакетов проекта
from loto import cli
from loto import model
from loto import utils


class Controller:
    """
    Управляющий класс игры.
    """
    def __init__(self, view: cli.View):
        self.view = view
        self.game: model.Game

    def set_game(self):
        """Управляет настройкой партии."""
        model.Human.number = 1
        model.Bot.number = 1
        players: list[model.Player] = []
        while True:
            players_str = self.view.get_players()
            for player in players_str.split(utils.SEP):
                player = player.replace('ё', 'е')
                if utils.pat_human.fullmatch(player):
                    players += [model.Human()]
                elif utils.pat_bot_easy.fullmatch(player):
                    players += [model.Bot(lvl=utils.DifficultyLvl.EASY)]
                elif utils.pat_bot_hard.fullmatch(player):
                    players += [model.Bot(lvl=utils.DifficultyLvl.HARD)]
            if len(players) >= 2:
                break
        self.game = model.Game(*players)

    def start_game(self) -> None:
        """Управляет игровым процессом партии."""
        while token := self.game.get_token:
            self.view.show_token(token)
            for player in self.game.players:
                self.view.show_card(player)
                if player.__class__ is model.Human:
                    res = player.action(token, self.get_human_turn())
                else:
                    res = player.action(token)
                    self.view.show_bot_action(player)
                if res:
                    self.view.show_winner(player)
                    return
            cont = self.game.check_fail()
            if cont == 1:
                self.view.show_winner(self.game.players[0])
                return
            elif cont == 0:
                self.view.show_tie()
                return

    def get_human_turn(self) -> utils.Answer:
        """Ход игрока-человека."""
        answer: str = self.view.get_turn()
        if answer in utils.Answer.YES.value:
            return utils.Answer.YES
        else:
            return utils.Answer.NO

