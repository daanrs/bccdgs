from thesis.conversion import pcalg_to_pag, pag_to_pcalg

import pandas as pd
import numpy as np

BCCD_RESULT = "data/in/bccd_result.csv"
ORIGINAL_PAG = "data/in/original_pag.csv"
LST_FILE = "data/in/lst.csv"
RESULT_PAG = "data/out/pag.csv"

def read_pag(file):
    """Read the PAG from a csv file"""
    df = (
        pd.read_csv(file, sep=',', header=None)
        .to_numpy()
    )

    return df

def read_lst(file):
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

    # removing all the zero probability statements
    df = df[df[:, 0] > 0.8]

    return df

def write_mag_as_pcalg(g, file):
    g = pag_to_pcalg(g)
    pd.DataFrame(g).to_csv(file, header=False, index = False)
    return

def bccd_result():
    return read_pag(BCCD_RESULT)

def original_pag():
    g = read_pag(ORIGINAL_PAG)
    return pcalg_to_pag(g)

def result_pag():
    g = read_pag(RESULT_PAG)
    return pcalg_to_pag(g)

def lst():
    return read_lst(LST_FILE)
