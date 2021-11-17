from conversion import pag_to_mag
from new_mag import adjacent_mags
from read_data import read_pag, read_lst
from score import score

import numpy as np

def main(pag, lst, max_iter=1000000, delta=0):
    mag = pag_to_mag(pag.copy())

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

    return mag

def get_new_mag(mag, lst):
    """
    Returns an adjacent mag with the maximum score.
    """
    mags = adjacent_mags(mag)
    mag_score = [score(m, lst) for m in mags]

    max_mag = np.argmax(mag_score)

    return mags[max_mag]
