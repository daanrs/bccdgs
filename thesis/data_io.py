import pandas as pd

def read_lst(file, prob_interval):
    """Read logical statements from a csv file.

    TODO: this makes a bunch of changes to the input"""
    df = (
        pd.read_csv(file, sep=',', header=None)
        .to_numpy()
        [:, [0, 2, 3, 4, 5]]
    )

    # reduce vertex indices by one since R uses 1...n instead of
    # 0...n-1
    df[:, 2:] -= 1

    # removing statements outside a certain probability interval
    min_prob, max_prob = prob_interval
    df = df[
        (df[:, 0] > min_prob)
        & (df[:, 0] < max_prob)
    ]

    # we do not handle these
    df = df[df[:, 1] != -4]
    df = df[df[:, 1] != -2]
    df = df[df[:, 1] != 3]
    df = df[df[:, 1] != 4]

    return df
