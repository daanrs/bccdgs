from thesis.score import score_dict
from thesis.util import (
    product_align, choices, add_edge_reverse,
    broadcast_concatenate,
    self_product_power
)
from thesis.graphs_array import graphs, graphs_tc, graphs_score

import numpy as np

def gen_new_mag(g, lst, n, k):
    """
    Generate the n best scoring mags with k edges changed.
    """
    # edges and marks to change for one graph
    marks = np.array([(0, 0), (1, 2), (2, 1), (2, 2)])
    edges = edges_from_shape(g.shape[0])

    # get new arrays of all edge and mark changes
    size, edges, marks = changes(marks, edges, k)
    gs = graphs(g, size, edges, marks)

    # remove all duplicates
    gs = np.unique(gs, axis=0)

    # graph transitive closure
    gst = graphs_tc(gs)

    # check if there is a path x -> ... -> y and x <-* y
    valids = ~ ((gst == 1) & (gs == 2)).any(axis=(1, 2))
    gs = gs[valids]
    gst = gst[valids]

    # we need size - n since we want the highest scoring mags
    sts = score_dict(lst)
    scores = graphs_score(gs, gst, sts)

    # get the n best mags, for which we partition the last n values
    n_scores = scores.size - n
    argp = np.argpartition(scores, n_scores)
    return gs[argp[n_scores:]]

def edges_from_shape(n):
    edges = choices(np.arange(n), 2)
    edges = add_edge_reverse(edges)

def changes(edges, marks, k):
    """
    Combine k edges and marks into a 3-tuple that specifies how we can
    perform a scatter on a graphs_array, and what size to perform it on.
    """
    edges = choices(edges, k)
    marks = self_product_power(marks, k)

    marks, edges = product_align(marks, edges)

    # the size is how many alternate graphs we're making
    size = edges.shape[0]

    # we add one index to edges to indicate which graph we're changing
    edges = broadcast_concatenate(np.arange(size), edges)

    edges = edges.reshape(-1, 3)
    marks = marks.reshape(-1)
    return size, edges, marks
