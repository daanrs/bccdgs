from thesis.conversion import dag_to_ancestral, to_directed
from thesis.score import score
from thesis.util import (
    product_align, choices, add_edge_reverse,
    broadcast_concatenate
)

import numpy as np

def gen_new_mag(g, lst, k):
    """
    Generate the best scoring mag with k edges changed.

    Note that this will not contain g.
    """
    size, edges, marks = changes(g, k)
    gs = big_array(g, size, edges, marks)

    #remove all copies of the original mag
    gs = gs[gs != g]

    # TODO: is this copy necessary?
    # graph transitive closure
    gst = gs.copy()
    gst = np.array([dag_to_ancestral(to_directed(g)) for g in gst])

    # check if there is a path x -> ... -> y and x <-* y
    valids = ~ ((gst == 1) & (gs == 2)).any(axis=(1, 2))
    gs = gs[valids]
    gst = gst[valids]

    scores = score(gst, gs, lst)
    return gs[np.argmax(scores)]

def changes(g, k):
    marks = np.array([(0, 0), (1, 2), (2, 1), (2, 2)])
    edges = choices(np.arange(g.shape[0]), 2)
    edges = add_edge_reverse(edges)

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
    size = edges[-1, 0] + 1
    return size, edges, marks

def big_array(g, size, edges, marks):
    if edges.shape[0] != marks.shape[0]:
        raise ValueError(
            "Edge and mark changes need the same size in dimension 0"
        )
    b = np.tile(g, (size,) + tuple(np.repeat(1, len(g.shape))))
    b[edges[:, 0], edges[:, 1], edges[:, 2]] = marks
    return b
