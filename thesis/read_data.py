import pandas as pd
import numpy as np

def read_pag(file):
    df = (
        pd.read_csv(file, sep='\s+', header=None)
        .to_numpy()
    )

    return df

def read_scst(file):
    df = (
        pd.read_csv(file, sep='\s+', header=None)
        .to_numpy()
        [:, [0, 2, 3, 4, 5]]
    )

    return df
