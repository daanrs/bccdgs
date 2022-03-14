from thesis.conversion import dag_to_ancestral, to_directed
from thesis.score import score
from thesis.util import (
    product_align, choices, add_edge_reverse,
    broadcast_concatenate
)

import numpy as np

def gen_new_mag(gs, lst, n, k):
    """
    Generate the n best scoring mags with k edges changed.
    """
    size, edges, marks = changes(gs, k)
    gs = big_array(gs, size, edges, marks)

    # remove all duplicates
    gs = np.unique(gs, axis=0)

    # graph transitive closure
    gst = np.array([dag_to_ancestral(to_directed(g)) for g in gs])

    # check if there is a path x -> ... -> y and x <-* y
    valids = ~ ((gst == 1) & (gs == 2)).any(axis=(1, 2))
    gs = gs[valids]
    gst = gst[valids]

    # we need size - n since we want the highest scoring mags
    n = score.size - n
    scores = score(gst, gs, lst)
    argp = np.argpartition(scores, n)
    return gs[argp[n:]]

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

    edges = np.broadcast_to(edges, gs.shape[:1] + edges.shape)
    marks = np.broadcast_to(marks, gs.shape[:1] + marks.shape)

    edges = broadcast_concatenate(
        np.arange(gs.shape[0]),
        edges
    )

    edges = edges.reshape(-1, 4)
    marks = marks.reshape(-1)
    size = edges[-1, 1] + 1
    return size, edges, marks

def big_array(gs, size, edges, marks):
    if edges.shape[0] != marks.shape[0]:
        raise ValueError(
            "Edge and mark changes need the same size in dimension 0"
        )

    newshape = np.array(gs.shape[:1] + (1,) + gs.shape[1:])
    gs = gs.reshape(tuple(newshape))

    newshape[:] = 1
    newshape[1] = size

    b = np.tile(gs, tuple(newshape))

    b[edges[:, 0], edges[:, 1], edges[:, 2], edges[:, 3]] = marks
    return b.reshape(-1, gs.shape[-1], gs.shape[-2])
