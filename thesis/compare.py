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
