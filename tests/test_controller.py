# импорт из модулей/пакетов стандартной библиотеки
from decimal import Decimal as dec
from pytest import mark
from statistics import mean

# импорт модулей/пакетов проекта
from loto.cli import View
from loto.controller import Controller
from loto.model.players import Human, Bot
from loto.model.card import Token
from loto.utils.data import SAMPLE_LENGTH


test_players = {
    'и_и': [Human, Human],
    'и_и_и': [Human, Human, Human],
    'и_бл': [Human, Bot],
    'бл_и': [Bot, Human],
    'и_бс_и_бл': [Human, Bot, Human, Bot],
}


class TestSetGame:

    app = Controller(View())

    @mark.parametrize('mock_cli', test_players.keys(), indirect=True)
    def test_players(self, mock_cli):
        self.app.set_game()
        result = [pl.__class__ for pl in self.app.game.players]
        assert result == test_players[mock_cli]


class TestBotGames:

    app = Controller(View())

    @mark.parametrize('mock_cli', ['бл_бс'], indirect=True)
    def test_duel_bot(self, mock_cli):
        all_turns = Token.maximum - Token.minimum
        results = []
        for _ in range(SAMPLE_LENGTH):
            self.app.set_game()
            self.app.start_game()
            results += [len(self.app.game._purse) / all_turns]
        results_mean = round(mean(results), 2)
        print(f'\n\n{results_mean = }\n')
        assert results_mean >= dec('0.65')
        # assert dec('0.09') <= pstdev(results, results_mean) <= dec('0.11')

