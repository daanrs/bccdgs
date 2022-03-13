from thesis.conversion import dag_to_ancestral, to_directed
from thesis.score import score
from thesis.util import (
    product_align, choices, add_edge_reverse,
    broadcast_concatenate
)

import numpy as np

from numba import njit

def gen_new_mag(g, lst, k):
    """
    Generate all valid mags which can be created through changing a single
    edge.
    """
    # all possible mark combinations
    edges, marks = changes(g, k)
    size = edges[-1, 0] + 1
    b = big_array(g, size, edges, marks)
    b = np.array([g for g in  b if valid_mag(g)])
    s = np.argmax(np.array([score(g, lst) for g in b]))
    return b[s]

def changes(g, k):
    # if keep_skeleton:
        # # TODO: these edges are not ordered correctly
        # marks = np.array([(1, 2), (2, 1), (2, 2)])
        # edges = np.transpose(np.nonzero(g))
    # else:
    marks = np.array([(0, 0), (1, 2), (2, 1), (2, 2)])
    nodes = choices(np.arange(g.shape[0]), 2)
    edges = add_edge_reverse(nodes)

    marks, edges = product_align(
        choices(marks, k),
        choices(edges, k)
    )
    edges = broadcast_concatenate(
        np.arange(edges.shape[0]),
        edges
    )
    edges = edges.reshape(-1, 3)
    marks = marks.reshape(-1)
    return edges, marks

def big_array(g, size, edges, marks):
    if edges.shape[0] != marks.shape[0]:
        raise ValueError(
            "Edge and mark changes need the same size in dimension 0"
        )
    b = np.tile(g, (size,) + tuple(np.repeat(1, len(g.shape))))
    b[edges[:, 0], edges[:, 1], edges[:, 2]] = marks
    return b

@njit
def valid_mag(mag):
    """
    Check if a mag has any (almost) directed cycles
    """
    # we get all possible directed paths from the mags transitive closure
    ancestral = dag_to_ancestral(to_directed(mag.copy()))

    # check if there is an adjacent path x -> ... -> y and x <-* y
    return not ((ancestral == 1) & (mag == 2)).any()
