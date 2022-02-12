from thesis.conversion import dag_to_ancestral, to_directed
from thesis.score import score

import numpy as np
import numba

def gen_new_mag(mag, lst, keep_skeleton):
    """
    Generate all valid mags which can be created through changing a single
    edge.
    """
    new_mag = mag.copy()

    # we loop over all possible (i, j) edges, making sure not to double
    # count (i, j) and (j, i)
    n = mag.shape[0]
    for i in np.arange(1, n):
        for j in np.arange(0, i):

            # if we want to keep the skeleton then we only make changes if
            # the original mag has an edge there
            if (not keep_skeleton) or (mag[i, j] != 0 and mag[j, i] != 0):
                mags = adjacent_mags(mag, i, j, keep_skeleton)
                mags = np.concatenate([mags, [new_mag]], axis=0)

                mag_score = [score(m, lst) for m in mags]
                best_mag = np.argmax(mag_score)
                new_mag = mags[best_mag]

    return new_mag

def adjacent_mags(mag, i, j, keep_skeleton):
    """
    Generate array of mags with all i *-* j possibilities
    """
    # one of the following is the same as the original mag
    mag_arrow_tail = mag.copy()
    mag_arrow_tail[i, j] = 2
    mag_arrow_tail[j, i] = 1

    mag_tail_arrow = mag.copy()
    mag_tail_arrow[i, j] = 1
    mag_tail_arrow[j, i] = 2

    mag_arrow_arrow = mag.copy()
    mag_arrow_arrow[i, j] = 2
    mag_arrow_arrow[j, i] = 2

    if not keep_skeleton:
        mag_no_edge = mag.copy()
        mag_no_edge[i, j] = 0
        mag_no_edge[j, i] = 0

        mags = np.array([
            mag_arrow_tail,
            mag_tail_arrow,
            mag_arrow_arrow,
            mag_no_edge
        ])
    else:
        mags = np.array([
            mag_arrow_tail,
            mag_tail_arrow,
            mag_arrow_arrow,
        ])

    # filter out the copy of the original mag
    is_original_mag = (mags == mag).all(axis=(1, 2))
    mags = mags[~is_original_mag]

    # filter out mags with cycles
    c = np.array([almost_directed_cycle(m) for m in mags])
    mags = mags[~c]

    return mags

def almost_directed_cycle(mag):
    """
    Check if a mag has any (almost) directed cycles
    """
    # we get all possible directed paths from the mags transitive closure
    ancestral = dag_to_ancestral(to_directed(mag.copy()))

    # check if there is an adjacent path x -> ... -> y and x <-* y
    return ((ancestral == 1) & (mag == 2)).any()
