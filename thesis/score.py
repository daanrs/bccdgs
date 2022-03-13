import numpy as np

def score(gst, gs, sts):
    """
    TODO: this function is fucked up
    [x,x,z] = unconditional indep. : c = -3;    z < x # confounder/paths
    [x,y,x] = x/>y         && x/>S : c = -1
    [x,x,z] = no edge x-z          : c =  0;    x < z
    [x,y,z] = x=>y || x=>z || x=>S : c = +1
    [x,y,y] = x=>y         || x=>S : c = +2

    scoring function = np.sum(np.log(1 - false_c) - np.log(false_c))

    statement = [c, score, x, y, z, ...]
    """
    if (
        (sts[:, 0] < -3)
        | (sts[:, 0] == -2)
        | (sts[:, 0] > 2)
    ).any():
        raise ValueError("Statement type not in (-3, -1, 0, 1, 2)")

    sts_cause_or = sts[sts[:, 0] == 2][:, 1:]
    sts_cause = sts[sts[:, 0] == 1][:, 1:]
    sts_edge = sts[sts[:, 0] == 0][:, 1:]
    sts_noncause = sts[sts[:, 0] == -1][:, 1:]
    sts_indep = sts[sts[:, 0] == -3][:, 1:]

    return (
        calc_score(
            s_cause(gst, sts_cause_or[:, [1, 2]])
            | s_cause(gst, sts_cause_or[:, [2, 3]]),
            sts_cause_or[:, 0]
        )
        + calc_score(s_cause(gst, sts_cause[:, [1, 2]]), sts_cause[:, 0])
        + calc_score(s_edge(gs, sts_edge[:, [1, 2]]), sts_edge[:, 0])
        + calc_score(~s_cause(gst, sts_noncause[:, [1, 2]]), sts_noncause[:, 0])
        + calc_score(s_indep(gst, gs, sts_indep[:, [1, 2]]), sts_indep[:, 0])
    )

def calc_score(gs_sts, sts):
    big_sts = np.broadcast_to(sts, gs_sts.shape)
    false_sts = big_sts[~gs_sts]
    return np.sum(np.log(1 - false_sts) - np.log(false_sts), axis=1)

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

