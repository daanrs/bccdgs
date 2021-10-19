import pandas as pd
import numpy as np

PAG_FILE = "../data/pag1.csv"
SCST_FILE = "../data/scst.csv"

def read_pag(file):
    """Reads the PAG from a csv file"""
    df = (
        pd.read_csv(file, sep='\s+', header=None)
        .to_numpy()
    )

    return df

def read_scst(file):
    """Reads scoring statements from a csv file.

    TODO: this currently makes a bunch of changes to the input"""
    df = (
        pd.read_csv(file, sep='\s+', header=None)
        .to_numpy()
        [:, [0, 2, 3, 4, 5]]
    )

    # reduce vertex indices by one since input uses 1...n instead of
    # 0...n-1
    df[:, 2:] -= 1

    # removing all the low probability statements, for now
    df = df[df[:, 0] > 0.1]

    return df
