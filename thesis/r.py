import numpy as np

import rpy2.robjects as ro
from rpy2.robjects.packages import importr
from rpy2.robjects import numpy2ri

numpy2ri.activate()

b = importr('bccdgsr')

def set_r_seed(s):
    b.set_seed(s)

def gen_graph(v, prob):
    return pcalg_to_pag(b.gen_graph(v, prob))

def run_bccd(g, l, n):
    g = pag_to_pcalg(g)
    c = b.get_cor(
        g,
        ro.IntVector(l),
        n
    )

    return pcalg_to_pag(b.run_bccd(c, n))

def get_pag(g, l):
    g = pag_to_pcalg(g)
    return pcalg_to_pag(b.get_pag(g, l))

def pag_to_mag(g):
    g = pag_to_pcalg(g)
    return pcalg_to_pag(b.pag_to_mag(g))

def mag_to_pag(g):
    g = pag_to_pcalg(g)
    return pcalg_to_pag(b.mag_to_pag(g))

def pag_to_pcalg(g):
    g = g.copy().T

    # switch circles and tails
    circles = g == 1
    tails = g == 3
    g[circles] = 3
    g[tails] = 1

    return g

def pcalg_to_pag(g):
    # transpose
    g = np.array(g)

    # switch circles and tails
    circles = g == 1
    tails = g == 3
    g[circles] = 3
    g[tails] = 1

    return g

