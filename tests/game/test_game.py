from pytest import mark, xfail

from loto.game.game import Game
from loto.game.players import Human, Bot
from loto.main import Controller
from loto.model.card import Token, Card
from loto.utils.data import GameMode, Answer
from loto.utils.errors import GameInitError


test_players = (
    (),
    (Human(), Human()),
    (Human(), Bot()),
    (Bot(), Bot()),
)
test_modes = (
    None,
    GameMode.PVP,
    GameMode.PVB,
    GameMode.BVB
)

def mock_get_next() -> Answer:
    return Answer.NO

test_card = (
    (1, 2, 3, 4, 5),
    (6, 7, 8, 9, 10),
    (11, 12, 13, 14, 15),
)


class TestGame:

    @mark.parametrize('players', test_players)
    @mark.parametrize('mode', test_modes)
    def test_init(self, players, mode):
        game = Game(*players, mode=mode)
        try:
            result_mode = game.mode
        except GameInitError as e:
            xfail(str(e))
        else:
            assert len(game.players) == 2
            # возможно, имеет смысл встроить этот тест в сам класс Game — например, под свойство game.ready -> bool
            result_players = {type(pl) for pl in game.players}
            if result_mode is GameMode.PVP:
                assert result_players == {Human}
            elif result_mode is GameMode.PVB:
                assert result_players == {Human, Bot}
            elif result_mode is GameMode.BVB:
                assert result_players == {Bot}

    @mark.parametrize('tokens_range', [(1, 90), (50, 150)])
    def test_purse(self, tokens_range: tuple[int, int]):
        Token.minimum, Token.maximum = tokens_range
        game = Game(mode=GameMode.PVP)
        amount = tokens_range[1] - tokens_range[0] + 1
        result = [game.get_token for _ in range(amount)]
        mn, mx = min(result), max(result)
        assert (mn, mx) == tokens_range

    def test_check_fail(self, monkeypatch):
        monkeypatch.setattr(Controller, 'get_input', mock_get_next)
        player1 = Human(Card(*test_card))
        player2 = Human(Card(*test_card))
        game = Game(player1, player2)
        player1.action(1)
        game.check_fail()
        assert player1 not in game.players

