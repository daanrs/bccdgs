from thesis.conversion import dag_to_ancestral, to_directed

import numpy as np
import numba

@numba.njit
def score(mag, lst):
    """
    Score how well a mag fits to lst.

    We use the score log(true_checks) + log(1 - false_checks), which is
    the log-hikelihood of this happening, and so higher is better.
    """
    # we need the transitive closure to compute some statements, and it is
    # much more efficient to calculate that once, then pass it on
    mag_tc = dag_to_ancestral(to_directed(mag.copy()))

    # we check which statments are correct
    # since lst = [prob, statement] we index it [:, 1:]
    smts = lst[:, 1:].astype(np.int8)
    checks =  np.array([statement(mag_tc, mag, s) for s in smts])

    # if checks is empty we return 0, since everything is true by default
    if len(checks) == 0:
        return 0
    else:
        # true_c = lst[checks][:, 0]
        false_c = lst[~checks][:, 0]
        # return np.sum(np.log(true_c)) + np.sum(np.log(1 - false_c))
        # return np.sum(np.log(1 - false_c))
        return np.sum(np.log(1 - false_c) - np.log(false_c))

@numba.njit
def statement(mag_tc, mag, statement):
    """
    Check whether a statement is correct.

    [x,x,z] = unconditional indep. : c = -3;    z < x # confounder/paths
    [x,y,x] = x/>y         && x/>S : c = -1
    [x,x,z] = no edge x-z          : c =  0;    x < z
    [x,y,z] = x=>y || x=>z || x=>S : c = +1
    [x,y,y] = x=>y         || x=>S : c = +2

    [x,y,y] = x=>y                 : c = +3 (only Binfo/LoCI stage)
    [x,y,x] = x/>y                 : c = -2 (only Binfo/LoCI stage)
    [x,x,x] =                 x=>S : c = +4
    [-,-,-] =                 x/>S : c = -4 (only Binfo/LoCI stage)
    """
    [c, x, y, z] = statement

    if c == -3:
        return not (
            ancestor(mag_tc, x, z)
            or ancestor(mag_tc, z, x)
            or cofounder(mag_tc, mag, x, z)
        )
    elif c == -1:
        return not ancestor(mag_tc, x, y)
    elif c == 0:
        return not edge(mag, x, z)
    elif c == 1:
        return ancestor(mag_tc, x, y) or ancestor(mag_tc, x, z)
    elif c == 2:
        return ancestor(mag_tc, x, y)
    else:
        raise ValueError('Statement type not in (-3, -1, 0, 1, 2)')

@numba.njit
def ancestor(mag_tc, x, y):
    """Check if x is an ancestor of y."""
    return (mag_tc[x, y] == 1)

@numba.njit
def edge(mag, x, y):
    """Check if there is an edge between x and y."""
    return (mag[x, y] != 0)

@numba.njit
def cofounder(mag_tc, mag, x, y):
    """Check if there is a cofounder between x and y."""
    # check for x <-> y
    if mag[x, y] == 2 and mag[y, x] == 2:
        return True
    # check for x <- ... <- z -> ... -> y
    else:
        return ((mag_tc[:, x] == 1) & (mag_tc[:, y] == 1)).any()
