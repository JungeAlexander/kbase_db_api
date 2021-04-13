import os
import sys

import pytest
from pytest import approx

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from db_api.crud import precision_recall_fscore


@pytest.mark.parametrize(
    "predicted,gold,precision,recall,fscore,tp,fp,fn",
    [
        ({(0, 1)}, {(0, 1)}, 1, 1, 1, 1, 0, 0),
        ({(0, 1)}, {(1, 2)}, 0, 0, 0, 0, 1, 1),
        (
            {(0, 1), (1, 2), (2, 3)},
            {(0, 1), (1, 2), (3, 4)},
            2 / 3,
            2 / 3,
            2 / 3,
            2,
            1,
            1,
        ),
    ],
)
def test_precision_recall_f1score(
    predicted, gold, precision, recall, fscore, tp, fp, fn
):
    precision_, recall_, fscore_, tp_, fp_, fn_ = precision_recall_fscore(
        predicted, gold
    )
    assert approx(precision_) == precision
    assert approx(recall_) == recall
    assert approx(fscore_) == fscore
    assert tp_ == tp
    assert fp_ == fp
    assert fn_ == fn
