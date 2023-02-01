from pytest import mark

from loto.model.card import Token


class TestToken:
    Token._minimum = 1
    Token._maximum = 90

    @mark.parametrize('number', [0, 1, -2, 34, 500])
    def test_is_int_within_range(self, number):
        obj = Token(number)
        assert isinstance(obj, int)
        if number < obj._minimum:
            assert obj == obj._minimum
        elif number > obj._maximum:
            assert obj == obj._maximum
        else:
            assert obj == number

    def test_set_of_tokens(self):
        result = {Token(1), Token(1)}
        assert result == {Token(1)}

    @mark.parametrize('number', [6, 78])
    def test_str_straight(self, number):
        obj = Token(number)
        width = len(str(obj._maximum))
        expected = f'{number:>{width}}'
        assert obj.__str__() == expected

    def test_str_strike(self):
        obj = Token()
        obj.strike = True
        width = len(str(obj._maximum))
        expected = '-'*width
        assert obj.__str__() == expected

