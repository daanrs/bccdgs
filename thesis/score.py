import numpy as np

def score(mag, scst):
    """
    TODO: implement
    """
    checks = np.array([ check_statement(mag, s) for s in scst[:, 1:] ])

    false_checks = scst[~checks]
    sc = np.sum(np.log(false_checks[:, 0]))

    return sc

def check_statement(mag, statement):
    """
    Checks whether a statement is correct.

    Currenly only checks statements for which c=1,2. Everything else
    returns True.
    """
    [c, x, y, z] = statement.astype(np.int64)

    # TODO: is this what we should be checking?
    # TODO: only checks 1, 2
    if c == 1 or c == 2 :
        b = (mag[y, x] == 2) | (mag[z, x] == 2)
    else:
        b = True
    return b
