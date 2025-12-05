# content of test_sample.py
def func(x):  # noqa: ANN001, ANN201
    return x + 1


def test_answer() -> None:
    assert func(3) == 5
