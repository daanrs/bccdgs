import graph_tool.all as gt
import numpy as np

# TODO: ensure everything is .copy()'d iff necessary

def pag_to_mag(pag):
    """Turns a pag into some reasonable mag. This MAG may not actually
    belong to the PAG's proper equivalence class."""
    pag = pag_create_arcs(pag)
    pag_directed = pag_only_directed_edges(pag.copy())

    pag_graph = adjacency_matrix_to_graph(pag_directed)
    tsort = gt.topological_sort(pag_graph)

    return orient_with_topological_sort(pag, tsort)

def pag_create_arcs(pag):
    """Returns a view with all possible circles turned into arcs; o-> and
    o-- are turned into --> and <-- respectively, o-o are left as they
    are."""
    # we select all circles
    circles = pag == 3

    # we transpose the array to check the other part of the edge
    arrows_t = pag.T == 2
    tails_t = pag.T == 1

    # select edges with circles and arrows/tails, then orient circle marks
    pag[circles & arrows_t] = 1
    pag[circles & tails_t] = 2
    return pag

def pag_only_directed_edges(pag):
    """Takes a pag and returns a view with only its directed edges"""
    tails = pag == 1
    arrows_t = pag.T == 2

    # set pag[i, j] = 1 iff i --> j; everything else to 0
    pag[tails & arrows_t] = 1
    pag[~(tails & arrows_t)] = 0
    return pag

def adjacency_matrix_to_graph(matrix):
    """Takes a directed adjacency matrix and returns a gt.Graph"""
    g = gt.Graph()

    edges = np.stack(np.nonzero(matrix), axis=1)

    g.add_edge_list(edges)

    return g

def orient_with_topological_sort(pag, tsort):
    """Returns a view of the PAG with all o-o circle edges turned into
    arcs according to the topological sort."""
    for i in tsort:
        for j in np.arange(0, len(pag)):
            if pag[i, j] == 3 and pag[j, i] == 3:
                pag[i, j] = 1
                pag[j, i] = 2
    return pag
