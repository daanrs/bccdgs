from conversion import pag_to_mag
from new_mag import adjacent_mags
from read_data import read_pag, read_scst
from score import score

import numpy as np

def main(pag, scst, max_iter=1000000, delta=0):
    mag = pag_to_mag(pag)

    new_mag = get_new_mag(mag, scst)
    n = 0

    while (score(new_mag, scst) > score(mag, scst) + delta) and (n <= max_iter):
        mag = new_mag.copy()
        new_mag = get_new_mag(new_mag, scst)
        n += 1

    # TODO: this should return a PAG
    return mag

def get_new_mag(mag, scst):
    """
    Returns an adjacent mag with the maximum score.
    """
    mags = adjacent_mags(mag)
    mag_score = [score(m, scst) for m in mags]

    max_mag = np.argmax(mag_score)

    return mags[max_mag]
