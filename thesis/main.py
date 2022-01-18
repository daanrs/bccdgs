from conversion import pag_to_mag
from new_mag import adjacent_mags
from score import score

from read_data import *

import numpy as np

def main(original_mag, pag, lst, max_iter=1000, delta=0):
    bccd_mag = pag_to_mag(pag.copy())
    mag = pag_to_mag(bccd_mag.copy())

    new_mag = get_new_mag(mag, lst)
    n = 0

    print(str(score(mag, lst)) + " -> " + str(score(new_mag, lst)))
    while (
            (score(new_mag, lst) > score(mag, lst) + delta)
            and (n <= max_iter)
    ):
        mag = new_mag.copy()
        new_mag = get_new_mag(new_mag, lst)
        n += 1
        print(str(score(mag, lst)) + " -> " + str(score(new_mag, lst)))

    print("bccd: " + str(compare_mags(bccd_mag, original_mag)))
    print("new: " + str(compare_mags(mag, original_mag)))
    return mag

def get_new_mag(mag, lst):
    """
    Return an adjacent mag with the best score.

    Currently this is the minimum score, as it is implemented as a
    penalty.
    """
    mags = adjacent_mags(mag)
    mag_score = [score(m, lst) for m in mags]

    best_mag = np.argmax(mag_score)

    return mags[best_mag]

def compare_mags(g1, g2):
    """
    Compare two different mags, returning how many edges are the same,
    normalized by their total number of edges
    """
    total = ((g1 != 0) | (g2 != 0)).sum()
    same = ((g1 == g2) & (g1 != 0) & (g2 != 0)).sum()
    return same/total

x = main(original_mag(), bccd_result(), lst())
print(original_mag())
print(bccd_result())
print(pag_to_mag(bccd_result()))
print(x)
