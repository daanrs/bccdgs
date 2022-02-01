from thesis.conversion import pcalg_to_pag, pag_to_pcalg

import pandas as pd
import numpy as np

def read_pag(file):
    """Read the PAG from a csv file"""
    df = (
        pd.read_csv(file, sep=',', header=None)
        .to_numpy()
    )

    return pcalg_to_pag(df)

def read_dag(file):
    """Read the PAG from a csv file"""
    df = (
        pd.read_csv(file, sep=',', header=None)
        .to_numpy()
    )
    return df

def read_lst(file, prob_interval):
    """Read logical statements from a csv file.

    TODO: this currently makes a bunch of changes to the input"""
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

def write_mag_as_pcalg(g, file):
    g = pag_to_pcalg(g)
    pd.DataFrame(g).to_csv(file, header=False, index = False)
    return

def read_lv(file):
    """
    Read latent variables
    """
    return pd.read_csv(file, header=None).to_numpy().flatten() - 1
