from thesis.score import *

import numpy as np

def test_score_dict():
    inp = np.array([
        [0.5, -3, 0, 1, 2],
        [0.5, -1, 0, 1, 2],
        [0.5, 0, 0, 1, 2],
        [0.5, 1, 0, 1, 2],
        [0.5, 2, 0, 1, 2]
    ])

    expected = {
        "cause_or": (
            (np.array([[0, 1]]), np.array([[1, 2]])),
            np.array([0.5])
        ),
        "cause" : (np.array([[0, 1]]), np.array([0.5])),
        "edge" : (np.array([[0, 2]]), np.array([0.5])),
        "noncause" : (np.array([[0, 1]]), np.array([0.5])),
        "indep" : (np.array([[0, 2]]), np.array([0.5])),
    }

    output = score_dict(inp)
    np.testing.assert_equal(output, expected)


def test_score():
    cause_or = (np.array([[0, 1]]), np.array([0.5]))
    pass
