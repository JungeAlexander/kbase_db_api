import os
import sys

from pytest import approx

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from db_api.crud import precision_recall_fscore


def test_precision_recall_f1score():
    assert approx(0.9) == 1.0
