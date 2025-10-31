import pytest

def divide(a, b):
    return a / b  # body from original snippet

def test_divide():
    assert divide(6, 2) == 3
    assert divide(10, 5) == 2
    with pytest.raises(ZeroDivisionError):
        divide(1, 0)
