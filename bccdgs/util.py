import numpy as np
import numba

def mag_to_ancestral(g):
    return dag_to_ancestral(to_directed(g))

@numba.njit
def to_directed(g):
    g = g.copy()
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
def dag_to_ancestral(g):
    g = g.copy()
    """
    Return the transitive closure of a dag
    """
    # fill the diagonal, so we can use matrix power to get the paths
    np.fill_diagonal(g, 1)

    # calculate the transitive closure by taking g^n
    n = g.shape[0]
    g = np.linalg.matrix_power(g, n)

    # change all non-zeros to one, and set diagonal back to 0
    for i in range(g.shape[0]):
        for j in range(g.shape[1]):
            if i == j:
                g[i, j] = 0
            elif g[i, j] != 0:
                g[i, j] = 1

    return g

def remove_latent_variables(g, lv):
    """
    Remove latent variables from a g
    """
    g = np.delete(g, lv, axis=0)
    g = np.delete(g, lv, axis=1)
    return g

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

def compare_pags(g1, g2):
    """
    Compare two different mags, returning how many edges are the same,
    normalized by their total number of edges
    """
    total = ((g1 != 0) | (g2 != 0)).sum()
    same = ((g1 == g2) & (g1 != 0) & (g2 != 0)).sum()
    return same/total

def compare_skeletons(g1, g2):
    """
    Compare the skeletons between two graphs.
    """
    g1 = g1.copy()
    g2 = g2.copy()
    g1[g1 != 0] = 1
    g2[g2 != 0] = 1
    return compare_pags(g1, g2)

def compare_causal_structure(pag, ancestral_dag):
    """
    Compare the causal structure of a pag with its ancestral dag.
    The ancestral dag is the result of
    remove_latent_variables(dag_to_ancestral(dag)).
    """
    arrows = pag == 2
    tails = pag == 1

    correct_tails = (ancestral_dag[tails] == 1).sum()
    correct_arrows = (ancestral_dag[arrows] == 0).sum()

    total = (tails | arrows).sum()

    return (correct_tails + correct_arrows)/total

