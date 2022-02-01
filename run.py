from thesis.main import main
from thesis.data_io import (
    write_mag_as_pcalg,
    read_pag,
    read_lst, read_lv, read_dag)
from thesis.compare import compare, compare_causal_structure
from thesis.conversion import remove_latent_variables, dag_to_ancestral

from pathlib import Path

import numpy as np
import pandas as pd
import subprocess

# HIDDEN      = "1"
# PROBABILITY = "0.6"
# NODES       = "5"

HIDDEN      = "2"
PROBABILITY = "0.25"
NODES       = "10"

# HIDDEN      = "3"
# PROBABILITY = "0.16"
# NODES       = "15"

# HIDDEN      = "4"
# PROBABILITY = "0.12"
# NODES       = "20"

def gen(m, keep_file=True):
    for i in m:
        p = Path(f"data/{NODES}/{i:03}/dag.csv")
        if not p.is_file() or not keep_file:
            p.parent.mkdir(parents = True, exist_ok = True)
            subprocess.run([
                "Rscript",
                "R/gen_graph.R",
                HIDDEN,
                PROBABILITY,
                NODES,
                f"data/{NODES}/{i:03}/lv.csv",
                f"data/{NODES}/{i:03}/dag.csv",
                f"data/{NODES}/{i:03}/pag.csv"
            ])

def bccd(m, n, keep_file=True):
    for i in m:
        for j in n:
            if not Path(f"data/{NODES}/{i:03}/{j:07}_bpag.csv").is_file() or not keep_file:
                subprocess.run([
                    "Rscript",
                    "R/run_bccd.R",
                    f"{j:07}",
                    f"data/{NODES}/{i:03}/lv.csv",
                    f"data/{NODES}/{i:03}/dag.csv",
                    f"data/{NODES}/{i:03}/{j:07}_fci.csv",
                    f"data/{NODES}/{i:03}/{j:07}_bccd.csv",
                    f"data/{NODES}/{i:03}/{j:07}_lst.csv",
                ],)

                bccd_location = f"data/{NODES}/{i:03}/{j:07}_bccd.csv"
                bmag_location = f"data/{NODES}/{i:03}/{j:07}_bmag.csv"
                bpag_location = f"data/{NODES}/{i:03}/{j:07}_bpag.csv"

                pag_to_mag(bccd_location, bmag_location)
                mag_to_pag(bmag_location, bpag_location)

def mag_to_pag(mag_location, pag_location):
    subprocess.run([
        "Rscript",
        "R/mag_to_pag.R",
        mag_location,
        pag_location
    ])

def pag_to_mag(pag_location, mag_location):
    subprocess.run([
        "Rscript",
        "R/pag_to_mag.R",
        pag_location,
        mag_location
    ])

def run(m, n, prob_interval, keep_skeleton, keep_file=True):
    for i in m:
        for j in n:
            mag_location = f"data/{prob_interval}/{keep_skeleton}/{NODES}/{i:03}/{j:07}_mag.csv"
            pag_location = f"data/{prob_interval}/{keep_skeleton}/{NODES}/{i:03}/{j:07}_pag.csv"
            bmag_location = f"data/{NODES}/{i:03}/{j:07}_bmag.csv"
            lst_location = f"data/{NODES}/{i:03}/{j:07}_lst.csv"

            if not Path(pag_location).is_file() or not keep_file:
                # if mag is empty we must generate new model and re-do
                # bccd and run on that part
                while Path(bmag_location).read_text() == '':
                    print("regenerating {NODES}/{i}")
                    gen([i], keep_file=False)
                    bccd([i], n, keep_file=False)
                    run([i], n, prob_interval, keep_skeleton,
                        keep_file=False)
                # make parent folder
                Path(pag_location).parent.mkdir(parents = True, exist_ok = True)

                bmag = read_pag(bmag_location)
                lst = read_lst(lst_location, prob_interval)
                mag = main(bmag, lst, keep_skeleton)

                write_mag_as_pcalg(mag, mag_location)
                mag_to_pag(mag_location, pag_location)

def compare_results(m, n, p, s):
    df = pd.DataFrame(columns=["n", "bccd", "result", "bccd_to_mag_to_pag"])
    for j in n:
        results = np.array([
            [compare(bccd_result(i, j), original_pag(i)),
             compare(bpag(i, j), original_pag(i)),
             compare(result_pag(i, j, p, s), original_pag(i))]
            for i in m ])

        # c = np.isnan(results).any(axis=(1, 2))
        c = np.isnan(results).any(axis=(1))
        scores = results[~c].mean(axis=0)
        df2 = pd.DataFrame([[j, scores[0], scores[1], scores[2]]]
                           , columns=["n", "bccd", "bccd_to_mag_to_pag", "result"]
                           )

        df = df.append(df2)
    # df = df.set_index("n").stack().unstack(0)
    return df

def compare_causal(m, n, p, s):
    df = pd.DataFrame(columns=["n", "bccd", "result", "bccd_to_mag_to_pag"])
    for j in n:
        results = np.array([
            [compare_causal_structure(bccd_result(i, j), ancestral_dag(i)),
             compare_causal_structure(bpag(i, j), ancestral_dag(i)),
             compare_causal_structure(result_pag(i, j, p, s), ancestral_dag(i))]
            for i in m ])

        # c = np.isnan(results).any(axis=(1, 2))
        c = np.isnan(results).any(axis=(1))
        scores = results[~c].mean(axis=0)
        df2 = pd.DataFrame([[j, scores[0], scores[1], scores[2]]]
                           , columns=["n", "bccd", "bccd_to_mag_to_pag", "result"]
                           )

        df = df.append(df2)
    # df = df.set_index("n").stack().unstack(0)
    return df

def write_results(m, n, p, s):
    df = compare_results(m, n, p, s)
    path = Path(f"data/results/{NODES}_{p}_{s}.csv")
    path.parent.mkdir(exist_ok = True)
    df.to_csv(path, index=False)
    return df

def bccd_result(i, j):
    g = read_pag(f"data/{NODES}/{i:03}/{j:07}_bccd.csv")
    return g

def bpag(i, j):
    g = read_pag(f"data/{NODES}/{i:03}/{j:07}_bpag.csv")
    return g

def original_pag(i):
    g = read_pag(f"data/{NODES}/{i:03}/pag.csv")
    return g

def ancestral_dag(i):
    g = read_dag(f"data/{NODES}/{i:03}/dag.csv")
    lv = read_lv(f"data/{NODES}/{i:03}/lv.csv")

    g = remove_latent_variables(dag_to_ancestral(g), lv)
    return g

def result_pag(i, j, p, s):
    g = read_pag(f"data/{p}/{s}/{NODES}/{i:03}/{j:07}_pag.csv")
    return g
