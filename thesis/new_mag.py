from conversion import adjacency_matrix_to_graph, pag_only_directed_edges

import graph_tool.all as gt
import numpy as np

def adjacent_mags(mag):
    # we need a non-empty array for np.concatenate to work properly
    mags = np.array([mag])

    n = mag.shape[0]
    for i in np.arange(1, n):
        for j in np.arange(0, i):
            # one of the following is the same as the original mag, we
            # filter that out later; TODO: do that more efficiently
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
    """Checks if a mag has any (almost) directed cycles"""
    mag = mag.copy()
    mag_directed = pag_only_directed_edges(mag.copy())
    g = adjacency_matrix_to_graph(mag_directed)

    paths = gt.transitive_closure(g).get_edges()

    # TODO: why does this indexing work exactly
    cycles = (mag[paths[:, 1], paths[:, 0]] == 2).any()

    return cycles
