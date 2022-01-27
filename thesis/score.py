from thesis.conversion import numpy_to_gt, to_directed

import graph_tool.all as gt
import numpy as np

def score(mag, lst):
    """
    Score how well a mag fits to lst.

    This sums statements which return false, with the value being
    abs(ln(p) - ln(1-p)).

    Higher score is better because log of a low probability gives a higher
    absolute value
    """
    checks = np.array([statement(mag, s) for s in lst[:, 1:]])

    # if checks > 0 this makes sense, otherwise everything is false
    if len(checks) > 0:
        true_c = lst[checks][:, 0]
        false_c = lst[~checks][:, 0]
    else:
        false_c = lst[:, 0]
        sc = np.abs(np.sum(np.log(1 - false_c)))
        return sc

    # if something with prob 0 is true, or prob 1 is false, then score = 0
    if (true_c == 0).any() or (false_c == 1).any():
        sc = -np.inf
    else:
        # sc = np.sum(
                # np.log(false_c) - np.log(1 - false_c)
        # )
        sc = np.abs(
            np.sum(np.log(true_c)) + np.sum(np.log(1 - false_c))
        )
    return sc

def statement(mag, statement):
    """
    Check whether a statement is correct.

    [x,y,z] = x=>y || x=>z || x=>S : c = +1
    [x,y,y] = x=>y         || x=>S : c = +2
    [x,y,y] = x=>y                 : c = +3 (only Binfo/LoCI stage)
    [x,y,x] = x/>y         && x/>S : c = -1
    [x,y,x] = x/>y                 : c = -2 (only Binfo/LoCI stage)
    [x,x,z] = no edge x-z          : c =  0;    x < z
    [x,x,z] = unconditional indep. : c = -3;    z < x # confounder/paths
    [x,x,x] =                 x=>S : c = +4
    [-,-,-] =                 x/>S : c = -4 (only Binfo/LoCI stage)
    """
    [c, x, y, z] = statement.astype(np.int64)

    if c == -3:
        b = not (
            cofounder(mag, x, z)
            or ancestor(mag, x, z)
            or ancestor(mag, z, x)
        )
    elif c == -1:
        b = not ancestor(mag, x, y)
    elif c == 0:
        b = not edge(mag, x, z)
    elif c == 1:
        b = ancestor(mag, x, y) or ancestor(mag, x, z)
    elif c == 2:
        b = ancestor(mag, x, y)
    else:
        raise ValueError('Statement type not in (-3, -1, 0, 1, 2)')
    return b

def ancestor(mag, x, y):
    """Check if x is an ancestor of y."""
    # get transitive closure graph
    g = gt.transitive_closure(numpy_to_gt(to_directed(mag.copy())))

    # TODO: make this more efficient
    g = gt.adjacency(g).toarray().T

    if g.size > 0:
        return (g[x, y] == 1)
    else:
        return False

def edge(mag, x, y):
    """Check if there is an edge between x and y."""
    if mag.size > 0:
        return (mag[x, y] != 0)
    else:
        return False

def cofounder(mag, x, y):
    """ Check if there is a cofounder between x and y."""
    g = gt.transitive_closure(numpy_to_gt(to_directed(mag.copy())))

    # TODO: make this more efficient
    g = gt.adjacency(g).toarray().T

    b = False
    if g.size > 0:
        for i in np.arange(g.shape[0]):
            if (g[i, x] == 1) and (g[i, y] == 1):
                b = True

    return b
