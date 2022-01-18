from conversion import pag_to_mag
from new_mag import adjacent_mags
from score import score

import graph_tool.all as gt
import numpy as np

def main(pag, lst, max_iter=1000000, delta=0):
    original_mag = pag_to_mag(pag.copy())
    mag = pag_to_mag(original_mag.copy())

    new_mag = get_new_mag(mag, lst)
    n = 0

    while (
            (score(new_mag, lst) > score(mag, lst) + delta)
            and (n <= max_iter)
    ):
        print(str(score(mag, lst)) + " -> " + str(score(new_mag, lst)))
        mag = new_mag.copy()
        new_mag = get_new_mag(new_mag, lst)
        n += 1

    print(gt.similarity(original_mag, mag))
    return mag

def get_new_mag(mag, lst):
    """
    Return an adjacent mag with the best score.

    Currently this is the minimum score, as it is implemented as a
    penalty.
    """
    mags = adjacent_mags(mag)
    mag_score = [score(m, lst) for m in mags]

    best_mag = np.argmin(mag_score)

    return mags[best_mag]
