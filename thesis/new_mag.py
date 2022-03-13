from thesis.conversion import dag_to_ancestral, to_directed
from thesis.score import score
from thesis.util import (
    product_align, choices, add_edge_reverse,
    broadcast_concatenate
)

import numpy as np

def gen_new_mag(gs, lst, k):
    """
    Generate the best scoring mag with k edges changed.
    """
    size, edges, marks = changes(gs, k)
    gs = big_array(gs, size, edges, marks)

    #remove all copies of the original mag
    # gs = gs[gs != g]
    gs = np.unique(gs, axis=1)

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

def changes(gs, k):
    if gs.shape[-1] != gs.shape[-2]:
        raise ValueError("Array not symmetrical, so not a graph")
    marks = np.array([(0, 0), (1, 2), (2, 1), (2, 2)])
    edges = choices(np.arange(gs.shape[-1]), 2)
    edges = add_edge_reverse(edges)

    marks, edges = product_align(
        choices(marks, k),
        choices(edges, k)
    )
    edges = broadcast_concatenate(
        np.arange(edges.shape[0]),
        edges
    )

    # TODO: maybe not reshape?
    edges = np.reshape(
        np.broadcast_to(edges, gs.shape[:1] + edges.shape),
        (gs.shape[0] * edges.shape[0],) + edges.shape[1:]
    )

    edges = broadcast_concatenate(
        np.arange(edges.shape[0]),
        edges
    )
    edges = edges.reshape(-1, 4)
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
