import numpy as np


def score_dict(sts):
    """
    [x,y,y] = x=>y         || x=>S : c = +2
    [x,y,z] = x=>y || x=>z || x=>S : c = +1
    [x,x,z] = no no_edge x-z          : c =  0;    x < z
    [x,y,x] = x/>y         && x/>S : c = -1
    [x,x,z] = unconditional indep. : c = -3;    z < x # confounder/paths
    """

    # if ((sts[:, 1] < -3)
    # | (sts[:, 1] == -2)
    # | (sts[:, 1] > 2)
    # ).any():
    # raise ValueError("Statement type not in (-3, -1, 0, 1, 2)")

    sts_cause = sts[sts[:, 1] == 2]
    sts_cause_or = sts[sts[:, 1] == 1]
    sts_no_edge = sts[sts[:, 1] == 0]
    sts_noncause = sts[sts[:, 1] == -1]
    sts_indep = sts[sts[:, 1] == -3]

    return {
        "cause": sts_cause[:, [0, 2, 3]],
        "cause_or": sts_cause_or[:, [0, 2, 3, 2, 4]],
        "no_edge": sts_no_edge[:, [0, 2, 4]],
        "noncause": sts_noncause[:, [0, 2, 3]],
        "indep": sts_indep[:, [0, 2, 4]],
    }


def filter_min_score(sts, min_prob):
    return {k: s[s[:, 0] > min_prob] for k, s in sts.items()}


def score(g,
          gt,
          cause,
          cause_or,
          no_edge,
          noncause,
          indep):

    s = 0

    if cause.size > 0:
        s += calc_score(s_cause(gt, cause[:, 1:].astype(int)), cause[:, 0])

    if cause_or.size > 0:
        s += calc_score(s_cause_or(gt,
                        cause_or[:, 1:].astype(int)), cause_or[:, 0])

    if no_edge.size > 0:
        s += calc_score(s_no_edge(g,
                        no_edge[:, 1:].astype(int)), no_edge[:, 0])

    if noncause.size > 0:
        s += calc_score(s_noncause(gt,
                        noncause[:, 1:].astype(int)), noncause[:, 0])

    if indep.size > 0:
        s += calc_score(s_indep(g, gt, indep[:, 1:].astype(int)), indep[:, 0])

    return s


def calc_score(g_sts, sts_score):
    """
    scoring function = np.sum(np.log(1 - false_c) - np.log(false_c))
    """
    false_sts = sts_score[~g_sts]
    return np.sum(np.log(1 - false_sts) - np.log(false_sts))


def s_noncause(gt, sts):
    return ~s_cause(gt, sts)


def s_cause_or(gt, sts):
    return s_cause(gt, sts[:, [0, 1]]) | s_cause(gt, sts[:, [2, 3]])


def s_cause(gt, sts):
    return gt[sts[:, 0], sts[:, 1]] == 1


def s_no_edge(g, sts):
    return g[sts[:, 0], sts[:, 1]] == 0


def s_common_cause(gt, sts):
    return (
        (gt.T[sts[:, 0]] == 1)
        & (gt.T[sts[:, 1]] == 1)
    ).any(axis=1)


def s_indep(g, gt, sts):
    return ~ (
        # x *-* y
        ~ s_no_edge(g, sts)

        # x -> ... -> y
        | s_cause(gt, sts)

        # x <- ... <- y
        | s_cause(gt, sts[:, ::-1])

        # x <- ... <- z -> ... -> y
        | s_common_cause(gt, sts)
    )
