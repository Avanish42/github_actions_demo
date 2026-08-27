import pytest

from src.calculator import add


@pytest.mark.parametrize(
    ("first_number", "second_number", "expected"),
    [
        (2, 3, 5),
        (-4, 9, 5),
        (1.5, 2.5, 4.0),
    ],
)
def test_add_returns_sum(first_number, second_number, expected):
    assert add(first_number, second_number) == expected