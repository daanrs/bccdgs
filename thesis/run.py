import pandas as pd
import numpy as np

import random

from thesis.r import *
from pathlib import Path

def run(
    nodes = 10,
    edge_prob = 0.3,
    max_hidden_nodes = 2,
    # models = [1, 2],
    # samples = [2000],
    models = np.arange(100),
    samples = 2 ** np.arange(7, 18),
    min_prob = 0.5,
    skel = False,
    seed = 5,
    write = False,
    location = Path("data_new")
):

    random.seed(seed)
    set_r_seed(seed)

    df = (
        pd.DataFrame(
            {
                "nodes": nodes,
                "edge_prob" : edge_prob,
                "hidden_nodes": np.array(random.sample(
                    range(nodes), max_hidden_nodes
                )),
                "dag": gen_graph(nodes, edge_prob),
                "samples": samples,
                "min_sts_prob": min_prob,
                "skel": skel,
            }
            for _ in models
        )
        .explode("samples")
        .reset_index()
        .rename(columns={"index": "id"})
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
        df.to_pickle(f"{location}/{nodes}_{edge_prob}_{min_prob}_{skel}.pkl")

    return df

    # df = (
        # pd.DataFrame(
            # {
                # "nodes": n,
                # "edge_prob": prob,
                # "model": model,
                # "skel": sk,
                # "samples": sample,
                # "log_samples": np.log2(sample),
                # "lst": lst(n, prob, hid, model, sample, (min_prob, 1)),
                # "min_prob": min_prob,
                # "iter": iterations(n, prob, hid, model, sample, (min_prob, 1), sk),
                # "original_pag": original_pag(n, prob, hid, model),
                # "ancestral_dag": ancestral_dag(n, prob, hid, model),
                # "mag_type": magtype,
                # "mag": mag,
                # "pag_type": pagtype,
                # "pag": pag,
            # }
            # for n, prob, hid in model_args
            # for model in models
            # for sample in samples
            # for min_prob in min_probs
            # for sk in skel
            # for magtype, mag,
                # pagtype, pag in [
                # (
                    # "original_mag", original_mag(n, prob, hid, model),
                    # "bccd",  bccd_result(n, prob, hid, model, sample)
                # ),
                # (
                    # "bccd_mag", bccd_mag(n, prob, hid, model, sample),
                    # "bccd_magpag", bpag(n, prob, hid, model, sample)
                # ),
                # (
                    # "bopt_mag", bopt_mag(n, prob, hid, model, sample, (min_prob, 1), sk),
                    # "bccd_opt", result_pag(n, prob, hid, model, sample, (min_prob, 1), sk)
                # )
            # ]
        # ).assign(
            # # this is kinda annoying, but we want to calculate different
            # # scores and we need access to seperate columns to do so; that
            # # is why we have nested lambda functions, and aggregate it
            # # along axis=1
            # mag_score = lambda frame: frame.agg(
                # lambda row: score(row["mag"], row["lst"]),
                # axis=1
            # ),
            # pag_acc = lambda frame: frame.agg(
                # lambda row: compare_pags(row["pag"], row["original_pag"]),
                # axis=1
            # ),
            # causal_acc = lambda frame: frame.agg(
                # lambda row: compare_causal_structure(
                    # row["pag"],
                    # row["ancestral_dag"]
                # ),
                # axis=1
            # )
        # )
    # )
    # return df
