from bccdgs.score import score, filter_min_score
from bccdgs.util import (
    dag_to_ancestral, to_directed,
    mag_to_ancestral,
)

from numba import njit, prange

import numpy as np

def bccdgs(mag, sts, k, skeleton, min_prob, max_iter=1000, verbose=True):
    """
    Run greedy search on bccd results.

    Parameters
    ----------
    mag: np.array
        square array representing an adjacency matrix
    sts: dict
        dictionary of np.arrays detailing the bccd logical statements
    n: int
        how many best mags to return
    k: int
        how many changes to make in one step
    skeleton: bool
        whether to keep the graph skeleton
    min_prob: float
        what probability a statement needs to be to be taken into account
    """
    sts = filter_min_score(sts, min_prob)

    mag = mag.copy()
    mag_tc = mag_to_ancestral(mag)
    mag_score = score(mag, mag_tc, **sts)

    new_mag = gen_new_mag(mag, sts, k, skeleton)
    new_mag_tc = mag_to_ancestral(new_mag)
    new_mag_score = score(new_mag, new_mag_tc, **sts)
    it = 0
    if verbose:
        print(f"skel={skeleton}, k={k}, prob={min_prob}, "
              + f"it={it}: {mag_score} -> {new_mag_score}")

    while (new_mag_score > mag_score) and (it <= max_iter):
        mag = new_mag.copy()
        mag_tc = new_mag_tc
        mag_score = new_mag_score

        new_mag = gen_new_mag(mag, sts, k, skeleton)
        new_mag_tc = mag_to_ancestral(new_mag)
        new_mag_score = score(new_mag, new_mag_tc, **sts)
        it += 1
        if verbose:
            print(f"skel={skeleton}, k={k}, prob={min_prob}, "
                  + f"it={it}: {mag_score} -> {new_mag_score}")

    return mag, it

def gen_new_mag(g, sts, k, skeleton):
    """
    Generate the n best scoring mags with k edges changed.
    """
    g = g.copy()

    # edges and marks to change for one graph
    if skeleton:
        marks = np.array([(1, 2), (2, 1), (2, 2)])
        edges = edges_from_skeleton(g)
    else:
        marks = np.array([(0, 0), (1, 2), (2, 1), (2, 2)])
        edges = edges_from_shape(g.shape[0])

    # get new arrays of all edge and mark changes
    size, edges, marks = changes(edges, marks, k)
    gs = graphs(g, size, edges, marks)

    # remove all duplicates
    gs = np.unique(gs, axis=0)

    # graph transitive closure
    gst = graphs_tc(gs)

    # check if there is a path x -> ... -> y and x <-* y
    valids = ~ ((gst == 1) & (gs == 2)).any(axis=(1, 2))
    gs = gs[valids]
    gst = gst[valids]

    if gs.size == 0:
        return g
    else:
        scores = graphs_score(gs, gst, sts)
        return gs[np.argmax(scores)]

def graphs(g, size, edges, marks):
    if edges.shape[0] != marks.shape[0]:
        raise ValueError(
            "Edge and mark changes need the same size in dimension 0"
        )

    b = g[np.newaxis, ...].repeat(size, axis=0)
    b[edges[:, 0], edges[:, 1], edges[:, 2]] = marks
    return b.reshape(-1, g.shape[-2], g.shape[-1])

@njit(parallel=True)
# @njit
def graphs_tc(gs):
    gst = np.empty(gs.shape, dtype=np.int_)
    for i in prange(gst.shape[0]):
        gst[i] = dag_to_ancestral(to_directed(gs[i]))
    return gst

def graphs_score(gs, gst, sts):
    scores = np.empty(gs.shape[0], dtype=float)
    for i in range(scores.size):
        scores[i] = score(gs[i], gst[i], **sts)
    return scores

def edges_from_shape(n):
    edges = choices(np.arange(n), 2)
    return add_edge_reverse(edges)

def edges_from_skeleton(g):
    e = np.transpose(np.nonzero(g))
    e = e[e[:, 0] < e[:, 1]]
    return add_edge_reverse(e)

def add_edge_reverse(x):
    return np.concatenate(
        (
            x[:, np.newaxis, :],
            x[:, np.newaxis, ::-1]
        ),
        axis = 1
    )

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

def choices(n, k):
    """
    All k choose n combinations.
    """
    if (k < 1) or (k > len(n)):
        raise ValueError("We must have 1 <= k <= len(n)")
    elif k == 1:
        return n[:, np.newaxis, ...]
    else:
        return np.concatenate([
            np.concatenate(
                (
                    n_k_1 := choices(n[i+1:], k-1),
                    np.broadcast_to(
                        n[i],
                        (n_k_1.shape[0], 1) + n[i].shape
                    )
                ),
                axis = 1
            )
            for i in range(n.shape[0]-k+1)
        ])

def self_product_power(x, k):
    x = x[:, np.newaxis, ...]
    xi = x
    for _ in range(k-1):
        xi = np.concatenate(product_align(xi, x), axis=1)
    return xi

def broadcast_concatenate(x, y):
    # TODO: this function is cursed
    ys = np.array(y.shape)[::-1]
    ys[0] = 1
    ys = tuple(ys)
    x = np.broadcast_to(x, ys).T.reshape(ys[::-1])
    return np.concatenate((x, y), axis=-1)

def product_align(x, y):
    """
    Repeat x and y in such a way that concatenating x and y would return
    their product.

    Given x.shape = (x1, x2, ..., xn)
    and y.shape = (y1, y2, ..., yn)
    return xs and ys with shape (x1 * y1, x2, ...) (x1 * y1, y2, ...)
    """
    # repeat all rows y1 times
    xs = x.repeat(y.shape[0], axis=0)

    # repeat the whole x1 times by temporarily adding one axis
    ys = (
        y[np.newaxis, ...]
        .repeat(x.shape[0], axis=0)
        .reshape((-1,) + y.shape[1:])
    )
    return xs, ys
