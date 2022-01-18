from conversion import numpy_to_gt, to_directed

import graph_tool.all as gt
import numpy as np

def score(mag, lst):
    """
    Score how well a mag fits to lst.

    This penalizes statements which return false, with the penalty being
    abs(ln(p) - ln(1-p)).
    """
    checks = np.array([statement(mag, s) for s in lst[:, 1:]])

    # TODO: should this be on false checks?
    false_checks = lst[~checks]
    sc = np.sum(
        np.abs(
            np.log(false_checks[:, 0])
            -  np.log(1 - false_checks[:, 0])
        )
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

    # we need do to this because the encoding in R starts at 1
    # TODO: find a better way to do this
    x -= 1
    y -= 1
    z -= 1

    if c == -3:
        b = ~(
            cofounder(mag, x, y)
            or ancestor(mag, x, y)
            or ancestor(mag, y, x)
        )
    elif c == -1:
        b = ~ancestor(mag, x, y)
    elif c == 0:
        b = ~edge(mag, x, y)
    elif c == 1:
        b = ancestor(mag, x, y) or ancestor(mag, x, z)
    elif c == 2:
        b = ancestor(mag, x, y)
    else:
        b = True
    return b

def ancestor(mag, x, y):
    """Check if x is an ancestor of y."""
    # get transitive closure graph
    g = gt.transitive_closure(numpy_to_gt(to_directed(mag.copy())))

    # TODO: make this more efficient
    g = gt.adjacency(g).toarray()

    # TODO: maybe g[x, y]?
    if g.size > 0:
        return (g[y, x] == 1)
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
    g = gt.adjacency(g).toarray()

    # TODO: is this right?
    b = False
    if g.size > 0:
        for _ in np.arange(g.shape[0]):
            # TODO: should this be g[b, y] instead?
            if (g[x, b] == 1) and (g[y, b] == 1):
                b = True

    return b
