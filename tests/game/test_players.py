from decimal import Decimal as dec
from pytest import mark

from loto.game.players import Human, Bot
from loto.main import Controller
from loto.model.card import Card
from loto.utils.data import Answer, DifficultyLvl, SAMPLE_LENGTH



class TestHuman:

    @staticmethod
    def mock_get_next() -> Answer:
        return Answer.NO

    @staticmethod
    def mock_get_strike() -> Answer:
        return Answer.YES

    def test_init(self):
        player = Human()
        assert type(player.card) is Card
        assert bool(player.card) is False
        assert player.fail is False

    @mark.parametrize('get_card_clean', [(1, 90)], indirect=True)
    def test_action_next(self, monkeypatch, get_card_clean):
        monkeypatch.setattr(
            Controller,
            'get_input',
            self.mock_get_next
        )
        player = Human(get_card_clean)
        win = player.action(100)
        assert player.fail is False
        assert win is False

    @mark.parametrize('get_card_clean', [(1, 90)], indirect=True)
    def test_action_next_fail(self, monkeypatch, get_card_clean):
        monkeypatch.setattr(
            Controller,
            'get_input',
            self.mock_get_next
        )
        player = Human(get_card_clean)
        win = player.action(1)
        assert player.fail is True
        assert win is False

    @mark.parametrize('get_card_clean', [(1, 90)], indirect=True)
    def test_action_strike(self, monkeypatch, get_card_clean):
        monkeypatch.setattr(
            Controller,
            'get_input',
            self.mock_get_strike
        )
        player = Human(get_card_clean)
        win = player.action(1)
        assert player.fail is False
        assert win is False

    @mark.parametrize('get_card_clean', [(1, 90)], indirect=True)
    def test_action_strike_fail(self, monkeypatch, get_card_clean):
        monkeypatch.setattr(
            Controller,
            'get_input',
            self.mock_get_strike
        )
        player = Human(get_card_clean)
        win = player.action(100)
        assert player.fail is True
        assert win is False

    @mark.parametrize('get_card_one_token', [(1, 90)], indirect=True)
    def test_action_strike_win(self, monkeypatch, get_card_one_token):
        monkeypatch.setattr(
            Controller,
            'get_input',
            self.mock_get_strike
        )
        player = Human(get_card_one_token)
        win = player.action(15)
        assert player.fail is False
        assert win is True


class TestBot:

    def test_init(self):
        player = Bot()
        assert type(player.card) is Card
        assert bool(player.card) is False
        assert player.fail is False
        assert player._actions.count(True) == SAMPLE_LENGTH*DifficultyLvl.EASY
        player = Bot(lvl=DifficultyLvl.HARD)
        assert player._actions.count(True) == SAMPLE_LENGTH*DifficultyLvl.HARD

    @mark.parametrize('get_card_clean', [(1, 90)], indirect=True)
    def test_action_easy(self, get_card_clean):
        results = []
        for _ in range(SAMPLE_LENGTH//2):
            player = Bot(get_card_clean, lvl=DifficultyLvl.EASY)
            player.action(1)
            results += [player.fail]
        for _ in range(SAMPLE_LENGTH//2):
            player = Bot(get_card_clean, lvl=DifficultyLvl.EASY)
            player.action(100)
            results += [player.fail]
        correct_actions = results.count(False)
        # стандартное отклонение random.choice() > 1, поэтому разброс значений около мат.ожидания будет выше — отсюда поправка 0.97
        assert correct_actions >= SAMPLE_LENGTH*DifficultyLvl.EASY*dec('0.97')

    @mark.parametrize('get_card_clean', [(1, 90)], indirect=True)
    def test_action_hard(self, get_card_clean):
        results = []
        for _ in range(SAMPLE_LENGTH//2):
            player = Bot(get_card_clean, lvl=DifficultyLvl.HARD)
            player.action(1)
            results += [player.fail]
        for _ in range(SAMPLE_LENGTH//2):
            player = Bot(get_card_clean, lvl=DifficultyLvl.HARD)
            player.action(100)
            results += [player.fail]
        correct = results.count(False)
        assert correct == SAMPLE_LENGTH

