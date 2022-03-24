import numpy as np

import rpy2.robjects as ro
from rpy2.robjects.packages import importr
from rpy2.robjects import numpy2ri

numpy2ri.activate()

b = importr('bccdgsr')

def set_r_seed(s):
    b.set_seed(s)

def gen_graph(v, deg):
    prob = deg / (v - 1)
    return pcalg_to_dag(b.gen_graph(v, prob))

def run_bccd(g, l, n):
    g = dag_to_pcalg(g)

    # r indices start at 1. TODO: copy?
    l = l.copy() + 1

    c = b.get_cor(
        g,
        ro.IntVector(l),
        n
    )

    bpag, sts = b.run_bccd(c, n)
    bpag = pcalg_to_pag(bpag)

    # we only take what we care about
    sts = sts[:, [0, 2, 3, 4, 5]]
    # r indices start at 1
    sts[:, 2:] = sts[:, 2:] - 1

    return bpag, sts

def dag_to_pag(g, l):
    # r indices start at 1. TODO: copy?
    l = l.copy() + 1

    g = dag_to_pcalg(g)
    return pcalg_to_pag(b.get_pag(g, l))

def pag_to_mag(g):
    g = pag_to_pcalg(g)

    gp = b.pag_to_mag(g)
    if (gp == 0).all():
        return None
    else:
        return pcalg_to_pag(gp)

def mag_to_pag(g):
    g = pag_to_pcalg(g)
    return pcalg_to_pag(b.mag_to_pag(g))

def dag_to_pcalg(g):
    return g.copy().T

def pcalg_to_dag(g):
    return np.array(g).T

def pag_to_pcalg(g):
    g = g.copy().T

    # switch circles and tails
    circles = g == 1
    tails = g == 3
    g[circles] = 3
    g[tails] = 1

    return g

def pcalg_to_pag(g):
    g = np.array(g).T

    # switch circles and tails
    circles = g == 1
    tails = g == 3
    g[circles] = 3
    g[tails] = 1

    return g

