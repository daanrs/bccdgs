from thesis.conversion import dag_to_ancestral, to_directed
from thesis.score import score

from numba import njit

@njit
def gen_new_mag(mag, lst):
    """
    Generate all valid mags which can be created through changing a single
    edge.
    """
    # all possible mark combinations
    marks = [(0, 0), (1, 2), (2, 1), (2, 2)]

    n = mag.shape[0]
    best_mag = mag.copy()

    # we loop over all possible (i, j) edges, making sure not to double
    # count (i, j) and (j, i)
    for i in range(1, n):
        for j in range(0, i):
            for new_mag in adjacent_mags(mag, i, j, marks):
                # if any adjacent mag has a higher score, save that one
                if score(new_mag, lst) > score(best_mag, lst):
                    best_mag = new_mag

    # return the best mag we've found
    return best_mag

@njit
def adjacent_mags(mag, x, y, marks):
    """
    Generate array of mags with all i *-* j possibilities
    """
    # one of the following is the same as the original mag
    for i, j in marks:
        # if marks are different than in the original mag we create a
        # new mag
        if (mag[x, y] != i) or (mag[y, x] != j):
            m = mag.copy()
            m[x, y] = i
            m[y, x] = j

            # check if this is a valid mag
            if valid_mag(m):
                yield m

@njit
def valid_mag(mag):
    """
    Check if a mag has any (almost) directed cycles
    """
    # we get all possible directed paths from the mags transitive closure
    ancestral = dag_to_ancestral(to_directed(mag.copy()))

    # check if there is an adjacent path x -> ... -> y and x <-* y
    return not ((ancestral == 1) & (mag == 2)).any()
