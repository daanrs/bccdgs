import pandas as pd
import numpy as np

import random

from bccdgs.bccdgs import bccdgs
from bccdgs.util import (
    dag_to_ancestral,
    remove_latent_variables,
    compare_pags, compare_causal_structure
)
from bccdgs.r import *
from bccdgs.score import score_dict

def gen_df(nodes = 10,
           degree = 3,
           min_latent_variables = 1,
           max_latent_variables = 2,
           models = range(100),
           samples = 2 ** np.arange(7, 18),
           # models=[1],
           # samples=[4096],
           seed = 5):

    random.seed(seed)
    set_r_seed(seed)

    df = (
        pd.DataFrame(
            {
                "model": model,
                "nodes": nodes,
                "samples": samples,
                "degree" : degree,
                "latent_variables": np.array(random.sample(
                    range(nodes),
                    random.choice(range(
                        min_latent_variables,
                        max_latent_variables + 1
                    ))
                )),
                "dag": gen_graph(nodes, degree),
            }
            for model in models
        )
        .explode("samples")
        .reset_index(drop=True)
        .assign(
            original_pag=lambda frame: frame.apply(
                lambda row: dag_to_pag(row["dag"], row["latent_variables"]),
                axis=1
            ),
        )
    )

    return bccd_df(df)

def bccd_df(df):
    df = (
        df.assign(
            bccd_and_sts=lambda frame: frame.apply(
                lambda row: run_bccd(
                    row["dag"],
                    row["latent_variables"],
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
            mag=lambda frame: frame["pag"].apply(pag_to_mag),
            magtype="bccdmp"
        )
        .drop(columns=["pagtype", "pag"])
    )
    return df

def bccdgs_df(df, k, skeleton, min_prob):
    df = df[df["magtype"] == "bccdmp"]

    df =  (
        df.assign(
            k=k,
            skeleton=skeleton,
            min_prob=min_prob,
            bccdgs_and_iter=lambda frame: frame.apply(
                lambda row: bccdgs(
                    row["mag"],
                    row["sts"],
                    row["k"],
                    row["skeleton"],
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
            pag=lambda frame: frame["mag"].apply(mag_to_pag),
            pagtype=lambda frame: frame["magtype"]
        )
        .drop(columns=["magtype", "mag"])
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
                        row["latent_variables"]
                    )
                ),
                axis=1
            )
        )
        .drop(columns = [ "pag", "dag", "original_pag", "sts", "latent_variables"])
    )
    return df
