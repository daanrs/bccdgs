from thesis.data_io import read_pag, read_dag, read_lv
from thesis.conversion import dag_to_ancestral, remove_latent_variables
from thesis.compare import compare_pags, compare_causal_structure

import pandas as pd
import numpy as np

def compile_result(
    model_args = [(5, 0.6, 1), (10, 0.25, 2), (15, 0.16, 3)],
    models = np.arange(100),
    samples = 2 ** np.arange(7, 18),
    min_probs = [0.5],
    skel = False,
):
    df = pd.DataFrame(
        {
            "nodes" : n,
            "edge_prob" : prob,
            "model" : model,
            "samples" : sample,
            "min_prob" : min_prob,
            "original_pag" : original_pag(n, prob, hid, model),
            "ancestral_dag" : ancestral_dag(n, prob, hid, model),
            "iter" : iterations(n, prob, hid, model, sample, (min_prob, 1), skel),
            "bccd" : bccd_result(n, prob, hid, model, sample),
            "bccd_magpag" : bpag(n, prob, hid, model, sample),
            "bccd_opt" : result_pag(n, prob, hid, model, sample, (min_prob, 1), skel)
        }
        for n, prob, hid in model_args
        for model in models
        for sample in samples
        for min_prob in min_probs
    )
    return scores_df(df)

def scores_df(df, fci=False):
    if fci:
        r = ["fci", "bccd", "bccd_magpag", "bccd_opt"]
    else:
        r = ["bccd", "bccd_magpag", "bccd_opt"]
    df_scores = pd.concat(
        [ df.apply(lambda x:
                   compare_pags(x[s], x["original_pag"]), axis=1)
         for s in r ]
        + [ df.apply(lambda x:
                     compare_causal_structure(x[s], x["ancestral_dag"]), axis=1)
           for s in r],
        keys = [s + "_pag_acc" for s in r] + [s + "_causal_acc" for s in r],
        axis = 1
    )

    df = pd.concat([df, df_scores], axis=1)
    return df

def bccd_result(nodes, eprob, mhid, model, sample):
    g = read_pag(f"data/{nodes}_{eprob}_{mhid}/{model:03}/{sample:07}_bccd.csv")
    return g

def bpag(nodes, eprob, mhid, model, sample):
    g = read_pag(f"data/{nodes}_{eprob}_{mhid}/{model:03}/{sample:07}_bpag.csv")
    return g

def fci(nodes, eprob, mhid, model, sample):
    g = read_pag(f"data/{nodes}_{eprob}_{mhid}/{model:03}/{sample:07}_fci.csv")
    return g

def original_pag(nodes, eprob, mhid, model):
    g = read_pag(f"data/{nodes}_{eprob}_{mhid}/{model:03}/pag.csv")
    return g

def ancestral_dag(nodes, eprob, mhid, model):
    g = read_dag(f"data/{nodes}_{eprob}_{mhid}/{model:03}/dag.csv")
    lv = read_lv(f"data/{nodes}_{eprob}_{mhid}/{model:03}/lv.csv")

    g = remove_latent_variables(dag_to_ancestral(g), lv)
    return g

def result_pag(nodes, eprob, mhid, model, sample, p, s):
    g = read_pag(f"data/{p}/{s}/{nodes}_{eprob}_{mhid}/{model:03}/{sample:07}_pag.csv")
    return g

def iterations(nodes, eprob, mhid, model, sample, p, s):
    g = pd.read_csv(
        f"data/{p}/{s}/{nodes}_{eprob}_{mhid}/{model:03}/{sample:07}_iter.csv",
        header=None).to_numpy().flatten()[0]
    return g

