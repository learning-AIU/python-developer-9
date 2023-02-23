# импорт из модулей/пакетов стандартной библиотеки
from pytest import fixture

# импорт модулей/пакетов проекта
from loto.cli import View
from loto.model.card import Token, Card


test_card = (
    (1, 2, 3, 4, 5),
    (6, 7, 8, 9, 10),
    (11, 12, 13, 14, 15),
)


@fixture
def get_card_clean(request) -> Card:
    Token.minimum, Token.maximum = request.param
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


@fixture
def mock_cli(request, monkeypatch):

    def suppress_stdout(*args, **kwargs):
        return None

    for attr in dir(View):
        if attr.startswith('show'):
            monkeypatch.setattr(View, attr, suppress_stdout)

    def mock_get_players(*args, **kwargs) -> str:
        return request.param

    monkeypatch.setattr(View, 'get_players', mock_get_players)
    return request.param

