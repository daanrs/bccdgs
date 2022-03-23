import pandas as pd
import numpy as np

import random

from thesis.r import *
from pathlib import Path

def gen_data(
    nodes = 10,
    degree = 2,
    max_hidden_nodes = 2,
    models = [1, 2],
    samples = [4000],
    seed = 5,
    write = False,
    location = Path("data_new")
):

    random.seed(seed)
    set_r_seed(seed)

    df = (
        pd.DataFrame(
            {
                "model": model,
                "nodes": nodes,
                "degree" : degree,
                "hidden_nodes": np.array(random.sample(
                    range(nodes), max_hidden_nodes
                )),
                "dag": gen_graph(nodes, degree),
                "samples": samples,
            }
            for model in models
        )
        .explode("samples")
        .reset_index(drop=True)
        .assign(
            pag=lambda frame: frame.apply(
                lambda row: dag_to_pag(row["dag"], row["hidden_nodes"]),
                axis=1
            ),
            bccd_and_sts=lambda frame: frame.apply(
                lambda row: run_bccd(
                    row["dag"],
                    row["hidden_nodes"],
                    row["samples"]
                ),
                axis=1
            ),
            bccd=lambda frame: frame["bccd_and_sts"].apply(
                lambda elem: elem[0]
            ),
            sts=lambda frame: frame["bccd_and_sts"].apply(
                lambda elem: elem[1]
            ),
            bmag=lambda frame: frame["bccd"].apply(pag_to_mag),
        )
        .drop(columns=["bccd_and_sts"])
        .dropna()
        .assign(
            bpag=lambda frame: frame["bmag"].apply(mag_to_pag),
        )
    )

    if write:
        df.to_pickle(f"{location}/{nodes}_{degree}.pkl")

    return df
