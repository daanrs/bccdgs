from thesis.conversion import dag_to_ancestral, to_directed

import numpy as np

def score(mag, lst):
    """
    Score how well a mag fits to lst.

    We use the score log(true_checks) + log(1 - false_checks), which is
    the log-hikelihood of this happening, and so higher is better.
    """
    # we check which statments are correct
    # since lst = [prob, statement] we index it [:, 1:]
    checks = np.array([statement(mag, s) for s in lst[:, 1:]])

    # if checks is empty everything is false
    if len(checks) == 0:
        true_c = []
        false_c = lst[:, 0]
    else:
        true_c = lst[checks][:, 0]
        false_c = lst[~checks][:, 0]

    return np.sum(np.log(true_c)) + np.sum(np.log(1 - false_c))

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
    g = dag_to_ancestral(to_directed(mag.copy()))

    return (g[x, y] == 1)

def edge(mag, x, y):
    """Check if there is an edge between x and y."""
    return (mag[x, y] != 0)

def cofounder(mag, x, y):
    """Check if there is a cofounder between x and y."""
    g = dag_to_ancestral(to_directed(mag.copy()))

    for i in np.arange(g.shape[0]):
        if (g[i, x] == 1) and (g[i, y] == 1):
            return True

    return False
