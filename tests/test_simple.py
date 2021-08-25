import pytest


@pytest.fixture
def var1():
    yield 1


@pytest.fixture
def var2(var1):
    return 1 + var1


def division(a, b):
    # if a > 5:
    #     return a / b - 1
    return a / b


def test_fixture(var1, var2):
    assert division(var1, var2) == 0.5


@pytest.mark.parametrize('a,b,res', [
    (4, 2, 2),
    (6, 2, 3),
    (5, 2, 2.5)
])
def test_numeric(a, b, res, var1):
    assert division(a, b) == res


@pytest.mark.parametrize('a,b,res', [
    ('a', 2, TypeError),
    (5, 0, ZeroDivisionError),
    (int, int, TypeError)
])
def test_exs(a, b, res):
    with pytest.raises(res):
        division(a, b)
