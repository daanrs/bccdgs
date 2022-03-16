import numpy as np

def score_dict(sts):
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

def score(gst,
          gs,
          cause_or=None,
          cause=None,
          edge=None,
          noncause=None,
          indep=None):

    s = np.zeros(gst.shape[0])
    if (cause_or != None) and (cause_or[0].size > 0):
        s += calc_score(s_cause_or(gst, cause_or[0]), cause_or[1])
    if (cause != None) and (cause[0].size > 0):
        s += calc_score(s_cause(gst, cause[0]), cause[1])
    if (edge != None) and (edge[0].size > 0):
        s += calc_score(s_edge(gs, edge[0]), edge[1])
    if (noncause != None) and (noncause[0].size > 0):
        s += calc_score(s_noncause(gst, noncause[0]), noncause[1])
    if (indep != None) and (indep[0].size > 0):
        s += calc_score(s_indep(gst, gs, indep[0]), indep[1])

    return s

def calc_score(gs_sts, sts):
    """
    scoring function = np.sum(np.log(1 - false_c) - np.log(false_c))
    """
    big_sts = np.broadcast_to(sts, gs_sts.shape)
    false_sts = big_sts[~gs_sts]
    return np.sum(np.log(1 - false_sts) - np.log(false_sts), axis=1)

def s_noncause(gst, sts):
    return ~s_cause(gst, sts)

def s_cause_or(gst, sts):
    return s_cause(gst, sts[0]) | s_cause(gst, sts[1])

def s_cause(gst, sts):
    return gst[:, sts[:, 0], sts[:, 1]] == 1

def s_edge(gs, sts):
    return gs[:, sts[:, 0], sts[:, 1]] != 0

def s_indep(gst, gs, sts):
    return ~ (
        s_edge(gs, sts)
        | s_cause(gst, sts)
        | s_cause(gst, sts[:, ::-1])
        | (
            (gst[:, :, sts[:, 0]] == 1)
            & (gst[:, :, sts[:, 1]] == 1)
        ).any(axis=1)
    )

