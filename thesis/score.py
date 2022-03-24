import numpy as np

def score_dict(sts, min_prob):
    """
    [x,y,y] = x=>y         || x=>S : c = +2
    [x,y,z] = x=>y || x=>z || x=>S : c = +1
    [x,x,z] = no edge x-z          : c =  0;    x < z
    [x,y,x] = x/>y         && x/>S : c = -1
    [x,x,z] = unconditional indep. : c = -3;    z < x # confounder/paths
    """

    if ((sts[:, 0] < -3)
            | (sts[:, 0] == -2)
            | (sts[:, 0] > 2)
            ).any():
        raise ValueError("Statement type not in (-3, -1, 0, 1, 2)")

    # index 1 contains something we don't care about
    sts = np.delete(sts, [1], axis=1)

    # we only take the statements with min_prob > 0.5
    # TODO: this should be a seperate function on the dictionary
    sts = sts[sts[:, 0] > min_prob]

    sts_cause_or = sts[sts[:, 1] == 2]
    sts_cause = sts[sts[:, 1] == 1]
    sts_edge = sts[sts[:, 1] == 0]
    sts_noncause = sts[sts[:, 1] == -1]
    sts_indep = sts[sts[:, 1] == -3]

    return {
        "cause_or": (
            (
                sts_cause_or[:, [2, 3]].astype(int),
                sts_cause_or[:, [3, 4]].astype(int)
            ),
            sts_cause_or[:, 0]
        ),
        "cause" : (sts_cause[:, [2, 3]].astype(int), sts_cause[:, 0]),
        "edge" : (sts_edge[:, [2, 4]].astype(int), sts_edge[:, 0]),
        "noncause" : (sts_noncause[:, [2, 3]].astype(int), sts_noncause[:, 0]),
        "indep" : (sts_indep[:, [2, 4]].astype(int), sts_indep[:, 0])
    }

def score(g,
          gt,
          cause_or=None,
          cause=None,
          edge=None,
          noncause=None,
          indep=None):

    s = 0
    if (cause_or != None) and (cause_or[0][0].size > 0):
        s += calc_score(s_cause_or(gt, cause_or[0]), cause_or[1])

    if (cause != None) and (cause[0].size > 0):
        s += calc_score(s_cause(gt, cause[0]), cause[1])

    if (edge != None) and (edge[0].size > 0):
        s += calc_score(s_edge(g, edge[0]), edge[1])

    if (noncause != None) and (noncause[0].size > 0):
        s += calc_score(s_noncause(gt, noncause[0]), noncause[1])

    if (indep != None) and (indep[0].size > 0):
        s += calc_score(s_indep(g, gt, indep[0]), indep[1])

    return s

def calc_score(g_sts, sts_score):
    """
    scoring function = np.sum(np.log(1 - false_c) - np.log(false_c))
    """
    false_sts = sts_score[g_sts]
    return np.sum(np.log(1 - false_sts) - np.log(false_sts))

def s_noncause(gt, sts):
    return ~s_cause(gt, sts)

def s_cause_or(gt, sts):
    return s_cause(gt, sts[0]) | s_cause(gt, sts[1])

def s_cause(gt, sts):
    return gt[sts[:, 0], sts[:, 1]] == 1

def s_edge(g, sts):
    return g[sts[:, 0], sts[:, 1]] != 0

def s_indep(g, gt, sts):
    return ~ (
        # x *-* y
        s_edge(g, sts)

        # x -> ... -> y
        | s_cause(gt, sts)

        # x <- ... <- y
        | s_cause(gt, sts[:, ::-1])

        # x <- ... <- z -> ... -> y
        | (
            (gt[:, sts[:, 0]] == 1)
            & (gt[:, sts[:, 1]] == 1)
        ).any(axis=0)
    )

