from thesis.main import main
from thesis.data_io import write_mag_as_pcalg, read_pag, read_lst
from thesis.compare import compare
from thesis.conversion import pcalg_to_pag

from pathlib import Path
from multiprocessing import Process

import numpy as np
import subprocess

def gen(n, keep_file=True):
    proc = []
    for i in np.arange(n):
        if not Path(f"data/{i:03}_bccd_result.csv").is_file() or not keep_file:
            p = Process(target = subprocess.run, args = (
                (["Rscript", "R/generate_input.R", f"{i:03}"],)
            ))
            # subprocess.run(["Rscript", "R/generate_input.R", f"{i:03}"])
            p.start()
            proc.append(p)
    for p in proc:
        p.join()

def run(n, prob_interval, keep_skeleton):
    proc = []
    for i in np.arange(n):
        mag_location = f"data/{prob_interval}_{keep_skeleton}_{i:03}_mag.csv"
        pag_location = f"data/{prob_interval}_{keep_skeleton}_{i:03}_pag.csv"

        if not Path(pag_location).is_file():
            p = Process(target=run_one, args=(
                i,
                prob_interval,
                keep_skeleton,
                mag_location,
                pag_location
            ))
            p.start()
            proc.append(p)
    for p in proc:
        p.join()

def run_one(i, prob_interval, keep_skeleton, mag_location, pag_location):
    bccd = bccd_result(i)
    mag = main(bccd, lst(i, prob_interval), keep_skeleton)

    write_mag_as_pcalg(mag, mag_location)
    subprocess.run(["Rscript",
                    "R/mag_to_pag.R",
                    mag_location,
                    pag_location
                    ])


def compare_results(n, p, s):
    results = np.array([
        [compare(bccd_result(i), original_pag(i)),
         compare(result_pag(i, p, s), original_pag(i))]
        for i in np.arange(n) ])

    # avg = results.mean(axis=1)
    return results

def give_mean(n, p, s):
    x = compare_results(n, p, s)
    c = np.isnan(x).any(axis=(1, 2))
    return x[~c].mean(axis=0)

def all(n, prob_interval, keep_skeleton):
    gen(n)
    run(n, prob_interval, keep_skeleton)

def bccd_result(n):
    return read_pag(f"data/{n:03}_bccd_result.csv")

def original_pag(n):
    g = read_pag(f"data/{n:03}_original_pag.csv")
    return pcalg_to_pag(g)

def result_pag(n, p, s):
    g = read_pag(f"data/{p}_{s}_{n:03}_pag.csv")
    return pcalg_to_pag(g)

def lst(n, prob_interval):
    return read_lst(f"data/{n:03}_lst.csv", prob_interval)
