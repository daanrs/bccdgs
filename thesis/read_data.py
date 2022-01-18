from conversion import dag_to_mag

import pandas as pd
import numpy as np

BCCD_RESULT = "../data/bccd_result.csv"
LATENT_VARIABLES = "../data/latent_variables.csv"
ORIGINAL_DAG = "../data/original_dag.csv"
LST_FILE = "../data/lst.csv"

def read_pag(file):
    """Reads the PAG from a csv file"""
    df = (
        pd.read_csv(file, sep=',', header=None)
        .to_numpy()
    )

    return df

def read_lst(file):
    """Reads logical statements from a csv file.

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
    df = df[df[:, 0] > 0]

    return df

def read_latent_variables(file):
    df = pd.read_csv(file, sep=',', header=None).to_numpy().flatten()
    return df

def bccd_result():
    return read_pag(BCCD_RESULT)

def latent_variables():
    return read_latent_variables(LATENT_VARIABLES)

def original_mag():
    g = read_pag(ORIGINAL_DAG)
    lv = latent_variables()

    g[g != 0] = 1
    g = g.astype(int)

    return dag_to_mag(g, lv)

def lst():
    return read_lst(LST_FILE)
