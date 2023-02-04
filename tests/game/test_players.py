from pytest import fixture

from loto.game.players import Human
from loto.main import Controller
from loto.model.card import Card
from loto.utils.data import Answer


def mock_get_next() -> Answer:
    return Answer.NO

def mock_get_strike() -> Answer:
    return Answer.YES


test_card = (
    (1, 2, 3, 4, 5),
    (6, 7, 8, 9, 10),
    (11, 12, 13, 14, 15),
)

@fixture
def get_card_clean() -> Card:
    return Card(*test_card)

@fixture
def get_card_one_token() -> Card:
    card = Card(*test_card)
    t = 0
    for i in range(Card.cells):
        if card[i] is not None:
            if t < Card.tokens - 1:
                card[i].strike = True
                t += 1
            else:
                return card


class TestHuman:

    def test_init(self):
        player = Human()
        assert type(player.card) is Card
        assert bool(player.card) is False
        assert player.fail is False

    def test_action_next(self, monkeypatch, get_card_clean):
        monkeypatch.setattr(Controller, 'get_input', mock_get_next)
        player = Human(get_card_clean)
        win = player.action(100)
        assert player.fail is False
        assert win is False

    def test_action_next_fail(self, monkeypatch, get_card_clean):
        monkeypatch.setattr(Controller, 'get_input', mock_get_next)
        player = Human(get_card_clean)
        win = player.action(1)
        assert player.fail is True
        assert win is False

    def test_action_strike(self, monkeypatch, get_card_clean):
        monkeypatch.setattr(Controller, 'get_input', mock_get_strike)
        player = Human(get_card_clean)
        win = player.action(1)
        assert player.fail is False
        assert win is False

    def test_action_strike_fail(self, monkeypatch, get_card_clean):
        monkeypatch.setattr(Controller, 'get_input', mock_get_strike)
        player = Human(get_card_clean)
        win = player.action(100)
        assert player.fail is True
        assert win is False

    def test_action_strike_win(self, monkeypatch, get_card_one_token):
        monkeypatch.setattr(Controller, 'get_input', mock_get_strike)
        player = Human(get_card_one_token)
        win = player.action(15)
        assert player.fail is False
        assert win is True



