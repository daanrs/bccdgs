from thesis.conversion import numpy_to_gt, to_directed

import graph_tool.all as gt
import numpy as np

def adjacent_mags(mag):
    """
    Generate all valid mags which can be created through changing a single
    edge.

    TODO: implement this more efficiently.
    """
    # we need a non-empty array for np.concatenate to work properly
    mags = np.array([mag])

    n = mag.shape[0]
    for i in np.arange(1, n):
        for j in np.arange(0, i):
            # one of the following is the same as the original mag, we
            # filter that out later
            mag_arrow_tail = mag.copy()
            mag_arrow_tail[i, j] = 2
            mag_arrow_tail[j, i] = 1

            mag_tail_arrow = mag.copy()
            mag_tail_arrow[i, j] = 1
            mag_tail_arrow[j, i] = 2

            mag_arrow_arrow = mag.copy()
            mag_arrow_arrow[i, j] = 2
            mag_arrow_arrow[j, i] = 2

            mag_no_edge = mag.copy()
            mag_no_edge[i, j] = 0
            mag_no_edge[j, i] = 0

            mags = np.concatenate([mags,
                            [mag_arrow_tail],
                            [mag_tail_arrow],
                            [mag_arrow_arrow],
                            [mag_no_edge]],
                           axis=0
                           )

    # filter out all copies of the original mag
    is_original_mag = (mags == mag).all(axis=(1, 2))
    mags = mags[~is_original_mag]

    # filter out mags with cycles
    c = np.array([almost_directed_cycle(m) for m in mags])
    mags = mags[~c]

    return mags

def almost_directed_cycle(mag):
    """Check if a mag has any (almost) directed cycles"""
    mag_directed = to_directed(mag.copy())
    g = numpy_to_gt(mag_directed)

    paths = gt.transitive_closure(g).get_edges()

    # TODO: why does this indexing work exactly
    cycles = (mag[paths[:, 0], paths[:, 1]] == 2).any()

    return cycles
