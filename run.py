from thesis.main import main
from thesis.data_io import write_mag_as_pcalg, read_pag, read_lst
from thesis.compare import compare
from thesis.conversion import pcalg_to_pag

from pathlib import Path

import numpy as np
import pandas as pd
import subprocess

def gen(m, keep_file=True):
    for i in np.arange(m):
        if not Path(f"data/{i:03}_dag.csv").is_file() or not keep_file:
            subprocess.run([
                "Rscript",
                "R/gen_graph.R",
                f"data/{i:03}_lv.csv",
                f"data/{i:03}_dag.csv",
                f"data/{i:03}_pag.csv"
            ])

def bccd(m, n, keep_file=True):
    for i in np.arange(m):
        for j in n:
            if not Path(f"data/{i:03}_{j:07}_bccd.csv").is_file() or not keep_file:
                subprocess.run([
                    "Rscript",
                    "R/run_bccd.R",
                    f"{j:07}",
                    f"data/{i:03}_lv.csv",
                    f"data/{i:03}_dag.csv",
                    f"data/{i:03}_{j:07}_bccd.csv",
                    f"data/{i:03}_{j:07}_lst.csv",
                ],)

def run(m, n, prob_interval, keep_skeleton):
    for i in np.arange(m):
        for j in n:
            mag_location = f"data/{prob_interval}_{keep_skeleton}/{i:03}_{j:07}_mag.csv"
            pag_location = f"data/{prob_interval}_{keep_skeleton}/{i:03}_{j:07}_pag.csv"
            bccd_location = f"data/{i:03}_{j:07}_bccd.csv"
            lst_location = f"data/{i:03}_{j:07}_lst.csv"

            if not Path(pag_location).is_file():
                run_one(
                    prob_interval,
                    keep_skeleton,
                    mag_location,
                    pag_location,
                    bccd_location,
                    lst_location
                )

def run_one(prob_interval,
            keep_skeleton,
            mag_location,
            pag_location,
            bccd_location,
            lst_location
            ):
    bccd = read_pag(bccd_location)
    lst = read_lst(lst_location, prob_interval)
    mag = main(bccd, lst, keep_skeleton)

    write_mag_as_pcalg(mag, mag_location)
    subprocess.run(["Rscript",
                    "R/mag_to_pag.R",
                    mag_location,
                    pag_location
                    ])


def compare_results(m, n, p, s):
    df = pd.DataFrame(columns=["n", "bccd", "result"])
    for j in n:
        results = np.array([
            [compare(bccd_result(i, j), original_pag(i)),
             compare(result_pag(i, j, p, s), original_pag(i))]
            for i in np.arange(m) ])

        # c = np.isnan(results).any(axis=(1, 2))
        c = np.isnan(results).any(axis=(1))
        scores = results[~c].mean(axis=0)
        df2 = pd.DataFrame([[j, scores[0], scores[1]]]
                           , columns=["n", "bccd", "result"]
                           )

        df = df.append(df2)
    df = df.set_index("n").stack().unstack(0)
    df.to_csv(f"data/results/{p}_{s}.csv")
    return

def runc(m, n, p, s):
    run(m, n, p, s)
    compare_results(m, n, p, s)

# def give_mean(m, p, s):
    # x = compare_results(m, p, s)
    # return x[~c].mean(axis=0)

def bccd_result(m, n):
    g = read_pag(f"data/{m:03}_{n:07}_bccd.csv")
    return g

def original_pag(m):
    g = read_pag(f"data/{m:03}_pag.csv")
    return pcalg_to_pag(g)

def result_pag(m, n, p, s):
    g = read_pag(f"data/{p}_{s}/{m:03}_{n:07}_pag.csv")
    return pcalg_to_pag(g)
