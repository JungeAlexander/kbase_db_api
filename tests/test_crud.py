from pytest import approx


def test_precision_recall_f1score():
    assert approx(0.9) == 1.0
