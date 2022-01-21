from thesis.conversion import pag_to_mag
from thesis.new_mag import adjacent_mags
from thesis.score import score
from thesis.data_io import *

import numpy as np

def main(pag, lst, max_iter=1000, delta=0):
    mag = pag_to_mag(pag.copy())
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

    write_mag_as_pcalg(mag, 'data/mag.csv')
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
