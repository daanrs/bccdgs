import graph_tool.all as gt
import numpy as np

# TODO: ensure everything is .copy()'d iff necessary

def pag_to_mag(g):
    """
    Turn a PAG into some reasonable MAG.

    This MAG may not actually belong to the PAG's equivalence class.

    TODO: generate multiple alternatives
    """
    g = orient_arcs(g)
    g_directed = to_directed(g.copy())

    tsort = gt.topological_sort(numpy_to_gt(g_directed))

    return orient_with_topological_sort(g, tsort)

def pag_to_pcalg(g):
    #operation is symmetric
    return pcalg_to_pag(g)

def pcalg_to_pag(g):
    # transpose
    g = g.copy().T

    # switch circles and tails
    circles = g == 1
    tails = g == 3
    g[circles] = 3
    g[tails] = 1

    return g

def orient_arcs(g):
    """
    Return a view with all semi-arcs turned into arcs.

    o-> and o-- are turned into --> and <-- respectively, o-o are left as
    they are.
    """
    # we select all circles
    circles = g == 3

    # we transpose the array to check the other part of the edge
    arrows_t = g.T == 2
    tails_t = g.T == 1

    # select edges with circles and arrows/tails, then orient circle marks
    g[circles & arrows_t] = 1
    g[circles & tails_t] = 2
    return g

def to_directed(g):
    """
    Take a graph and return a view with only its directed edges.
    """
    tails = g == 1
    arrows_t = g.T == 2

    # set g[i, j] = 1 iff i --> j; everything else to 0
    g[tails & arrows_t] = 1
    g[~(tails & arrows_t)] = 0
    return g

def from_directed(g):
    """
    Takes a graph where [i, j] = 1 and returns one where [j, i] = 2 is
    added
    """
    arrows = g.T == 1
    g[arrows] = 2
    return g

def numpy_to_gt(matrix):
    """
    Take a numpy directed adjacency matrix and return a gt.Graph.
    """
    g = gt.Graph()

    edges = np.stack(np.nonzero(matrix), axis=1)

    g.add_edge_list(edges)

    return g

def orient_with_topological_sort(g, tsort):
    """
    Return a view of the PAG with all o-o circle edges turned into
    arcs according to the topological sort.
    """
    for i in tsort:
        for j in np.arange(0, len(g)):
            if g[i, j] == 3 and g[j, i] == 3:
                g[i, j] = 1
                g[j, i] = 2
    return g
