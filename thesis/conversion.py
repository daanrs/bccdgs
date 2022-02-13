import numpy as np
import numba

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

@numba.njit
def to_directed(g):
    """
    Take a graph and return a view with only its directed edges.
    """
    tails = g == 1
    arrows_t = g.T == 2

    # set g[i, j] = 1 iff i --> j; everything is 0
    g = np.zeros(g.shape)
    for i in range(g.shape[0]):
        for j in range(g.shape[1]):
            if tails[i, j] and arrows_t[i, j]:
                g[i, j] = 1
    return g

@numba.njit
def dag_to_ancestral(dag):
    """
    Return the transitive closure of a dag
    """
    # we fill the diagonal, so we can use matrix power to get the paths
    np.fill_diagonal(dag, 1)

    # then we calculate the transitive closure by taking dag^n
    n = dag.shape[0]
    dag = np.linalg.matrix_power(dag, n)

    # change all non-zeros to one
    for i in range(dag.size):
        if dag.flat[i] != 0:
            dag.flat[i] = 1
    return dag

def remove_latent_variables(dag, lv):
    """
    Remove latent variables from a dag
    """
    dag = np.delete(dag, lv, axis=0)
    dag = np.delete(dag, lv, axis=1)
    return dag

def dag_to_mag(dag, lv):
    """
    If Y latent, then change all X -> Y -> Z to X -> Z,
    and X <- Y -> Z to X <-> Z, and then remove Y from graph.

    We assume latent_variables is an array of indices, and dag is a
    adjacency matrix.
    """
    dag = dag.copy()
    # dag has values (eg. 0.3 or 0.01) that represent the relation between
    # nodes, we change it to just have a 1 if there is a relation
    dag[dag != 0] = 1

    # we change from dag format to mag format directed edges, so we must
    # add arrows to dag[j, i] = 2 for all i --> j
    dag = dag.astype(int)
    dag[dag.T == 1] = 2

    # add edges that implicitly carry the information from the latent
    # variables
    for i in lv:
        for j in np.arange(0, len(dag)):
            # if i -> j
            if dag[i, j] == 1:
                for k in np.arange(0, len(dag)):

                    # if k -> i -> j and no edge k, j then k -> j
                    if dag[k, i] == 1 and dag[k, j] == 0 and dag[j, k] == 0:
                        dag[k, j] = 1
                        dag[j, k] = 2

                    # if k <- i -> j and no edge k, j then k <-> j
                    elif dag[k, i] == 2 and dag[k, j] == 0 and dag[j, k] == 0:
                        dag[k, j] = 2
                        dag[j, k] = 2

    dag = remove_latent_variables(dag, lv)
    return dag
