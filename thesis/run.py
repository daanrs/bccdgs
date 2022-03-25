import pandas as pd
import numpy as np

import random

from thesis.bccdgs import bccdgs
from thesis.conversion import (
    dag_to_mag, dag_to_ancestral,
    remove_latent_variables
)
from thesis.r import *
from thesis.score import score_dict
from thesis.compare import compare_pags, compare_causal_structure

def gen_data(nodes = 10,
             degree = 3,
             max_hidden_nodes = 2,
             models = [1, 2],
             samples = [4000],
             seed = 5,):

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
            original_pag=lambda frame: frame.apply(
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
            pag=lambda frame: frame["bccd_and_sts"].apply(
                lambda elem: elem[0]
            ),
            pagtype="bccd",
            sts=lambda frame: frame["bccd_and_sts"].apply(
                lambda elem: score_dict(elem[1])
            ),
        )
        .drop(columns=["bccd_and_sts"])
    )
    return df

def mag_df(df):
    df = (
        df.assign(
            pag=lambda frame: frame["pag"].apply(pag_to_mag),
            pagtype="bccdmp"
        )
        .rename(columns={"pagtype": "magtype", "pag": "mag"})
    )
    return df

def bccdgs_df(df, n, k, min_prob):
    df =  (
        df[df["magtype"] == "bccdmp"]
        .assign(
            n=n,
            k=k,
            min_prob=min_prob,
            bccdgs_and_iter=lambda frame: frame.apply(
                lambda row: bccdgs(
                    row["mag"],
                    row["sts"],
                    row["n"],
                    row["k"],
                    row["min_prob"]
                ),
                axis = 1
            ),
            mag=lambda frame: frame["bccdgs_and_iter"].apply(
                lambda elem: elem[0]
            ),
            it=lambda frame: frame["bccdgs_and_iter"].apply(
                lambda elem: elem[1]
            ),
            magtype="bccdgs",
        )
        .drop(columns=["bccdgs_and_iter"])
    )
    return df

def pag_df(df):
    df = (
        df.assign(
            mag=lambda frame: frame["mag"].apply(mag_to_pag),
        )
        .rename(columns={"magtype": "pagtype", "mag": "pag"})
    )

    return df

def pag_score_df(df):
    df = (
        df.assign(
            pag_acc=lambda frame: frame.agg(
                lambda row: compare_pags(
                    row["original_pag"],
                    row["pag"]
                ),
                axis=1
            ),
            causal_acc = lambda frame: frame.agg(
                lambda row: compare_causal_structure(
                    row["pag"],
                    remove_latent_variables(
                        dag_to_ancestral(row["dag"].copy()),
                        row["hidden_nodes"]
                    )
                ),
                axis=1
            )
        )
        .drop(columns = [ "pag", "dag", "original_pag", "sts", "hidden_nodes"])
    )
    return df
