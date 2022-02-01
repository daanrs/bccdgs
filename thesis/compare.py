def compare(g1, g2):
    score1 = compare_pags(g1, g2)
    # score2 = compare_pags_noc(g1, g2)
    # score3 = compare_skeletons(g1, g2)
    # return np.array([score1, score2, score3])
    return score1

def compare_pags(g1, g2):
    """
    Compare two different mags, returning how many edges are the same,
    normalized by their total number of edges
    """
    total = ((g1 != 0) | (g2 != 0)).sum()
    same = ((g1 == g2) & (g1 != 0) & (g2 != 0)).sum()
    return same/total

def compare_pags_noc(g1, g2):
    """
    Compare two pags, removing circle marks
    """
    return compare_pags(remove_circle_marks(g1.copy()),
                        remove_circle_marks(g2.copy()))

def compare_skeletons(g1, g2):
    g1 = g1.copy()
    g2 = g2.copy()
    g1[g1 != 0] = 1
    g2[g2 != 0] = 1
    return compare_pags(g1, g2)

def remove_circle_marks(g):
    g[g == 3] = 0
    return g

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
