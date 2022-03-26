from bccdgs.score import *

import numpy as np

def test_score_dict():
    inp = np.array([
        [0.5, 2, 0, 1, 2],
        [0.6, 1, 0, 1, 2],
        [0.7, 0, 0, 1, 2],
        [0.8, -1, 0, 1, 2],
        [0.9, -3, 0, 1, 2]
    ], dtype=np.float_)
    print(inp)

    exp = {
        "cause" : np.array([[0.5, 0, 1]]),
        "cause_or": np.array([[0.6, 0, 1, 0, 2]]),
        "edge": np.array([[0.7, 0, 2]]),
        "noncause": np.array([[0.8, 0, 1]]),
        "indep": np.array([[0.9, 0, 2]])
    }

    outp = score_dict(inp)
    np.testing.assert_equal(outp, exp)

# def test_score():
    # cause_or = (np.array([[0, 1]]), np.array([0.5]))
    # pass
