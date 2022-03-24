import pandas as pd
import numpy as np

import random

from pathlib import Path

from thesis.bccdgs import bccdgs
from thesis.conversion import dag_to_mag
from thesis.r import *
from thesis.score import score_dict
# from thesis.compare import compare_pags, compare_causal_structure

def gen_data(
    nodes = 10,
    degree = 3,
    max_hidden_nodes = 2,
    models = [1, 2],
    samples = [4000],
    seed = 5,
    write = False,
    location = Path("data")
):

    random.seed(seed)
    set_r_seed(seed)

    df = (
        pd.DataFrame(
            {
                "model": model,
                "nodes": nodes,
                "samples": samples,
                "degree" : degree,
                "hidden_nodes": np.array(random.sample(
                    range(nodes), max_hidden_nodes
                )),
                "dag": gen_graph(nodes, degree),
            }
            for model in models
        )
        .explode("samples")
        .reset_index(drop=True)
        .assign(
            mag=lambda frame: frame.apply(
                lambda row: dag_to_mag(row["dag"], row["hidden_nodes"]),
                axis=1
            ),
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
                lambda elem: score_dict(elem[1])
            ),
            bccd_mag=lambda frame: frame["bccd"].apply(pag_to_mag),
        )
        .drop(columns=["bccd_and_sts"])
        .dropna()
        .assign(
            bccd_mp=lambda frame: frame["bccd_mag"].apply(mag_to_pag),
        )
    )

    if write:
        df.to_pickle(f"{location}/{nodes}_{degree}.pkl")

    return df

def run_bccdgs(df, n, k, min_prob):
    df =  (
        df.assign(
            n=n,
            k=k,
            min_prob=min_prob,
            bccdgs_and_iter=lambda frame: frame.apply(
                lambda row: bccdgs(
                    row["bccd_mag"],
                    row["sts"],
                    row["n"],
                    row["k"],
                    row["min_prob"]
                ),
                axis = 1
            ),
            bccdgs_mag=lambda frame: frame["bccdgs_and_iter"].apply(
                lambda elem: elem[0]
            ),
            it=lambda frame: frame["bccdgs_and_iter"].apply(
                lambda elem: elem[1]
            ),
            bccdgs = lambda frame: frame["bccdgs_mag"].apply(mag_to_pag)
        )
        .drop(columns=["bccdgs_and_iter"])
    )

    return df
