from thesis.data_io import (
    read_pag,
    read_dag,
    read_lst,
    read_lv,
    gen_loc,
    bccd_loc,
    run_loc
)
from thesis.conversion import (
    dag_to_ancestral, remove_latent_variables,
    dag_to_mag
)
from thesis.compare import compare_pags, compare_causal_structure
from thesis.score import score

import pandas as pd
import numpy as np

def get_result(
    model_args = [(10, 0.25, 2)],
    models = np.arange(50),
    samples = 2 ** np.arange(7, 18),
    min_probs = [0.5],
    skel = [False],
):
    df = (
        pd.DataFrame(
            {
                "nodes": n,
                "edge_prob": prob,
                "model": model,
                "skel": sk,
                "samples": sample,
                "log_samples": np.log2(sample),
                "lst": lst(n, prob, hid, model, sample, (min_prob, 1)),
                "min_prob": min_prob,
                "iter": iterations(n, prob, hid, model, sample, (min_prob, 1), sk),
                "original_pag": original_pag(n, prob, hid, model),
                "ancestral_dag": ancestral_dag(n, prob, hid, model),
                "mag_type": magtype,
                "mag": mag,
                "pag_type": pagtype,
                "pag": pag,
            }
            for n, prob, hid in model_args
            for model in models
            for sample in samples
            for min_prob in min_probs
            for sk in skel
            for magtype, mag,
                pagtype, pag in [
                (
                    "original_mag", original_mag(n, prob, hid, model),
                    "bccd",  bccd_result(n, prob, hid, model, sample)
                ),
                (
                    "bccd_mag", bccd_mag(n, prob, hid, model, sample),
                    "bccd_magpag", bpag(n, prob, hid, model, sample)
                ),
                (
                    "bopt_mag", bopt_mag(n, prob, hid, model, sample, (min_prob, 1), sk),
                    "bccd_opt", result_pag(n, prob, hid, model, sample, (min_prob, 1), sk)
                )
            ]
        ).assign(
            # this is kinda annoying, but we want to calculate different
            # scores and we need access to seperate columns to do so; that
            # is why we have nested lambda functions, and apply it along
            # axis=1
            mag_score = lambda frame: frame.apply(
                lambda row: score(row["mag"], row["lst"]),
                axis=1
            ),
            pag_acc = lambda frame: frame.apply(
                lambda row: compare_pags(row["pag"], row["original_pag"]),
                axis=1
            ),
            causal_acc = lambda frame: frame.apply(
                lambda row: compare_causal_structure(row["pag"],
                                                   row["ancestral_dag"]),
                axis=1
            )
        )
    )
    return df

def original_mag(*args):
    dag = read_dag(gen_loc(*args) + "dag.csv")
    lv = read_lv(gen_loc(*args) + "lv.csv")
    return dag_to_mag(dag, lv)

def lv(*args):
    return read_lv(gen_loc(*args) + "lv.csv")

def original_pag(*args):
    return read_pag(gen_loc(*args) + "pag.csv")

def bccd_result(*args):
    return read_pag(bccd_loc(*args) + "bccd.csv" )

def bpag(*args):
    return read_pag(bccd_loc(*args) + "bpag.csv")

def fci(*args):
    return read_pag(bccd_loc(*args) + "fci.csv")

def lst(n, prob, hid, model, sample, prob_interval):
    return read_lst(
        bccd_loc(n, prob, hid, model, sample) + "lst.csv",
        prob_interval
    )

def bccd_mag(*args):
    return read_pag(bccd_loc(*args) + "bmag.csv")

def bopt_mag(*args):
    return read_pag(run_loc(*args) + "mag.csv")

def ancestral_dag(*args):
    g = read_dag(gen_loc(*args) + "dag.csv")
    lv = read_lv(gen_loc(*args) + "lv.csv")

    return remove_latent_variables(dag_to_ancestral(g), lv)

def result_pag(*args):
    return read_pag(run_loc(*args) + "pag.csv")

def iterations(*args):
    return (
        pd.read_csv(
            run_loc(*args) + "iter.csv",
            header=None
        ).to_numpy()
        .flatten()
        [0]
    )
