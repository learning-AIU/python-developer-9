from pytest import mark

from loto.model.card import Token


class TestToken:
    minimum = 1
    maximum = 90

    @mark.parametrize('number', [0, 1, -2, 34, 500])
    def test_is_int_within_range(self, number):
        Token._minimum = self.minimum
        Token._maximum = self.maximum
        obj: Token = Token(number)
        assert isinstance(obj, int)
        if number < self.minimum:
            assert obj == obj._minimum
        elif number > self.maximum:
            assert obj == obj._maximum
        else:
            assert obj == number

    @mark.parametrize('number', [6, 78])
    def test_str_straight(self, number):
        Token._minimum = self.minimum
        Token._maximum = self.maximum
        obj = Token(number)
        width = len(str(obj._maximum))
        expected = f'{number:>{width}}'
        assert obj.__str__() == expected

    def test_str_strike(self):
        Token._minimum = self.minimum
        Token._maximum = self.maximum
        obj = Token()
        obj.strike = True
        width = len(str(self.maximum))
        expected = '-'*width
        assert obj.__str__() == expected
