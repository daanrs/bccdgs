from thesis.conversion import dag_to_ancestral, to_directed
from thesis.score import score

import numpy as np

from numba import njit

def graphs(g, size, edges, marks):
    if edges.shape[0] != marks.shape[0]:
        raise ValueError(
            "Edge and mark changes need the same size in dimension 0"
        )

    shape_to_tile = tuple(np.repeat(1, len(g.shape) + 1))
    shape_to_tile = (size,) + shape_to_tile

    b = np.tile(g, shape_to_tile)

    b[edges[:, 0], edges[:, 1], edges[:, 2]] = marks
    return b.reshape(-1, g.shape[-1], g.shape[-2])

@njit
def graphs_tc(gs):
    gst = gs.copy()
    for i in gst.shape[0]:
        gst[i] = dag_to_ancestral(to_directed(gst[i]))
    return gst

def graphs_score(gs, gst, sts):
    scores = np.empty(gs.shape[0], dtype=float)
    for i in range(scores.size):
        scores[i] = score(gs[i], gst[i], sts)
    return scores
