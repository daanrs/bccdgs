import graph_tool.all as gt
import numpy as np

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

    g.add_vertex(len(matrix))
    g.add_edge_list(edges)

    return g

def dag_to_ancestral(dag):
    """
    Return the transitive closure of a dag
    """
    g = gt.transitive_closure(numpy_to_gt(dag.copy()))

    g = gt.adjacency(g).toarray().T
    return g

def remove_latent_variables(dag, lv):
    """
    Remove latent variables from a dag
    """
    dag = np.delete(dag, lv, axis=0)
    dag = np.delete(dag, lv, axis=1)
    return dag
