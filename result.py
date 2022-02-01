from thesis.data_io import read_pag, read_dag, read_lv
from thesis.conversion import dag_to_ancestral, remove_latent_variables
from thesis.compare import compare_pags, compare_causal_structure

import pandas as pd
import numpy as np

def compile_result(
    nodes = [10],
    models = np.arange(40),
    samples = 2 ** np.arange(7, 18),
    min_probs = [0.5],
    skel = False
):
    df = pd.DataFrame(
        {
            "nodes" : n,
            "model" : model,
            "sample" : sample,
            "min_prob" : min_prob,
            "original_pag" : original_pag(n, model),
            "ancestral_dag" : ancestral_dag(n, model),
            "bccd" : bccd_result(n, model, sample),
            "fci" : fci(n, model, sample),
            "bpag" : bpag(n, model, sample),
            "result" : result_pag(n, model, sample, (min_prob, 1), skel)
        }
        for n in nodes
        for model in models
        for sample in samples
        for min_prob in min_probs
    )
    return scores_df(df)

def scores_df(df):
    r = ["bccd", "result", "bpag", "fci"]
    df_scores = pd.concat(
        [ df.apply(lambda x:
                   compare_pags(x[s], x["original_pag"]), axis=1)
         for s in r ]
        + [ df.apply(lambda x:
                     compare_causal_structure(x[s], x["ancestral_dag"]), axis=1)
           for s in r],
        keys = [s + "_acc" for s in r] + [s + "_css" for s in r],
        axis = 1
    )

    df = pd.concat([df, df_scores], axis=1)
    return df

def bccd_result(nodes, model, sample):
    g = read_pag(f"data/{nodes}/{model:03}/{sample:07}_bccd.csv")
    return g

def bpag(nodes, model, sample):
    g = read_pag(f"data/{nodes}/{model:03}/{sample:07}_bpag.csv")
    return g

def fci(nodes, model, sample):
    g = read_pag(f"data/{nodes}/{model:03}/{sample:07}_fci.csv")
    return g

def original_pag(nodes, model):
    g = read_pag(f"data/{nodes}/{model:03}/pag.csv")
    return g

def ancestral_dag(nodes, model):
    g = read_dag(f"data/{nodes}/{model:03}/dag.csv")
    lv = read_lv(f"data/{nodes}/{model:03}/lv.csv")

    g = remove_latent_variables(dag_to_ancestral(g), lv)
    return g

def result_pag(nodes, model, sample, p, s):
    g = read_pag(f"data/{p}/{s}/{nodes}/{model:03}/{sample:07}_pag.csv")
    return g
