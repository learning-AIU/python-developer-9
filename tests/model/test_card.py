from pytest import mark
from re import compile

from loto.model.card import Token, Row, Card


class TestToken:
    Token.minimum = 1
    Token.maximum = 90

    @mark.parametrize('number', [0, 1, -2, 34, 500])
    def test_is_int_within_range(self, number):
        obj = Token(number)
        assert isinstance(obj, int)
        if number < obj.minimum:
            assert obj == obj.minimum
        elif number > obj.maximum:
            assert obj == obj.maximum
        else:
            assert obj == number

    def test_set_of_tokens(self):
        result = {Token(1), Token(1)}
        assert result == {Token(1)}

    @mark.parametrize('number', [6, 78])
    def test_str_straight(self, number):
        obj = Token(number)
        width = len(str(obj.maximum))
        expected = f'{number:>{width}}'
        assert obj.__str__() == expected

    def test_str_strike(self):
        obj = Token()
        obj.strike = True
        width = len(str(obj.maximum))
        expected = '-'*width
        assert obj.__str__() == expected


test_row_numbers = (
    [1, 2, 3, 4, 5, 6, 7, 8, 9],
    [1, 2, 3],
    [1, 23, 3, 45, 6],
    [5, 3, 2, 4, 1],
    [10, 50, 30, 40, 20]
)

class TestRow:
    Row.cells = 9
    Row.tokens = 5

    @mark.parametrize('numbers', test_row_numbers[:3])
    def test_init(self, numbers):
        tokens = [Token(n) for n in numbers]
        try:
            row = Row(*tokens)
        except ValueError as e:
            msg = 'number of Row constructor arguments must equal Row.tokens'
            assert str(e) == msg
        else:
            assert isinstance(row, tuple)
            assert len(row) == Row.cells

    @mark.parametrize('numbers', test_row_numbers[2:])
    def test_sorted_tokens(self, numbers):
        tokens = [Token(n) for n in numbers]
        row = Row(*tokens)
        result = [t for t in row if isinstance(t, Token)]
        assert result == sorted(tokens)

    Token.minimum = 1
    Token.maximum = 90

    @mark.parametrize('n', range(5))
    def test_str(self, n):
        tokens = [Token() for _ in range(Row.tokens)]
        row = Row(*tokens)
        pattern = compile(r'(?:[ \d]\d| {2}) ?')
        expected = pattern.findall(row.__str__())
        assert len(expected) == Row.cells


class TestCard:
    Token.minimum = 1
    Token.maximum = 90

    Row.cells = 9
    Row.tokens = 5

    Card.rows = 3

    @mark.parametrize('rows', (test_row_numbers, test_row_numbers[2:]))
    def test_init(self, rows):
        try:
            card = Card(*rows)
        except ValueError as e:
            msg = 'number of Card constructor arguments must equal Card.rows'
            assert str(e) == msg
        else:
            assert isinstance(card, list)
            assert len(card) == Card.rows

    @mark.parametrize('n', range(10))
    def test_unique(self, n):
        card = Card()
        result = {t for r in card for t in r} - {None}
        assert len(result) == Row.tokens * Card.rows

    @mark.parametrize('n', range(3))
    def test_str(self, n):
        card = Card()
        pattern = compile(r'((?:(?:[ \d]\d| {2}) ?)+\n)')
        result = pattern.findall(card.__str__())
        assert len(result) == Card.rows

