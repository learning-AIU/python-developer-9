from multimethod import DispatchError
from pytest import mark, xfail

from loto.game.game import Game
from loto.game.players import Human, Bot
from loto.model.card import Token
from loto.utils.data import GameMode, Answer
from loto.utils.errors import GameInitError


test_players = (
    (),
    (Human(), Human()),
    (Human(), Bot()),
    (Bot(), Bot()),
    (Bot(), Human(), Bot()),
)
test_modes = (
    None,
    GameMode.PVP,
    GameMode.PVB,
    GameMode.BVB,
)

class TestGame:

    @mark.parametrize('players', test_players)
    def test_init_players(self, players):
        try:
            game = Game(*players)
        except (GameInitError, DispatchError) as e:
            xfail(str(e))
        else:
            # возможно, имеет смысл встроить этот тест в сам класс Game — например, под свойство game.ready -> bool
            result_players = {type(pl) for pl in game.players}
            if game.mode is GameMode.PVP:
                assert result_players == {Human}
            elif game.mode is GameMode.PVB:
                assert result_players == {Human, Bot}
            elif game.mode is GameMode.BVB:
                assert result_players == {Bot}

    @mark.parametrize('mode', test_modes)
    def test_init_modes(self, mode):
        try:
            game = Game(mode)
        except (GameInitError, DispatchError) as e:
            xfail(str(e))
        else:
            assert len(game.players) == Game.players_number
            result_players = {type(pl) for pl in game.players}
            if game.mode is GameMode.PVP:
                assert result_players == {Human}
            elif game.mode is GameMode.PVB:
                assert result_players == {Human, Bot}
            elif game.mode is GameMode.BVB:
                assert result_players == {Bot}

    @mark.parametrize('tokens_range', [(1, 90), (50, 150)])
    def test_purse(self, tokens_range: tuple[int, int]):
        Token.minimum, Token.maximum = tokens_range
        game = Game(GameMode.PVP)
        amount = tokens_range[1] - tokens_range[0] + 1
        result = [game.get_token for _ in range(amount)]
        mn, mx = min(result), max(result)
        assert (mn, mx) == tokens_range

    @mark.parametrize('get_card_clean', [(1, 90)], indirect=True)
    def test_check_fail(self, get_card_clean):
        player1 = Human(get_card_clean)
        player2 = Human(get_card_clean)
        game = Game(player1, player2)
        game.players[0].action(1, Answer.NO)
        game.check_fail()
        assert player1 not in game.players

