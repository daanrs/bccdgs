import rpy2.robjects as ro
from rpy2.robjects.packages import importr
from rpy2.robjects import numpy2ri
from rpy2.robjects.conversion import localconverter

b = importr('bccdgsr')

def set_r_seed(s):
    b.set_seed(s)

def gen_graph(v, deg):
    prob = deg / (v - 1)
    g = b.gen_graph(v, prob)
    with localconverter(ro.default_converter + numpy2ri.converter):
        g = ro.conversion.rpy2py(g)
    return g

def run_bccd(g, l, n):

    # r indices start at 1. TODO: copy?
    if l.size > 0:
        l = l.copy() + 1

    with localconverter(ro.default_converter + numpy2ri.converter):
        g = ro.conversion.py2rpy(g)
        l = ro.conversion.py2rpy(l)
        n = ro.conversion.py2rpy(n)

    c = b.get_cor(
        g,
        # ro.IntVector(l),
        l,
        n
    )

    bpag, sts, sts_use = b.run_bccd(c, n)

    with localconverter(ro.default_converter + numpy2ri.converter):
        bpag = ro.conversion.rpy2py(bpag)
        sts = ro.conversion.rpy2py(sts)
        # sts_use = ro.conversion.rpy2py(sts_use)

    # bpag = g_switch(bpag)

    # we only take what we care about
    sts = sts[:, [0, 2, 3, 4, 5]]
    # r indices start at 1
    sts[:, 2:] = sts[:, 2:] - 1

    return bpag, sts

def dag_to_pag(g, l):
    # r indices start at 1. TODO: copy?
    if l.size > 0:
        l = l.copy() + 1

    with localconverter(ro.default_converter + numpy2ri.converter):
        g = ro.conversion.py2rpy(g)
        l = ro.IntVector(l)

    gp = b.dag_to_pag(g, l)
    with localconverter(ro.default_converter + numpy2ri.converter):
        gp = ro.conversion.rpy2py(gp)

    return g_switch(gp)

def pag_to_mag(g):
    g = g_switch(g)

    with localconverter(ro.default_converter + numpy2ri.converter):
        g = ro.conversion.py2rpy(g)

    gm = b.pag_to_mag(g)
    with localconverter(ro.default_converter + numpy2ri.converter):
        gm = ro.conversion.rpy2py(gm)

    if (gm == 0).all():
        return None
    else:
        return g_switch(gm)

def mag_to_pag(g):
    g = g_switch(g)

    with localconverter(ro.default_converter + numpy2ri.converter):
        g = ro.conversion.py2rpy(g)

    gp = b.mag_to_pag(g)
    with localconverter(ro.default_converter + numpy2ri.converter):
        gp = ro.conversion.rpy2py(gp)

    return g_switch(gp)

def g_switch(g):
    """
    Switches between pcalg and bccd pag format
    """
    g = g.T.copy()

    # switch circles and tails
    circles = g == 1
    tails = g == 3
    g[circles] = 3
    g[tails] = 1

    return g
