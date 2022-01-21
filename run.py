from thesis.main import main
from thesis.data_io import write_mag_as_pcalg, read_pag, read_lst
from thesis.compare import compare
from thesis.conversion import pcalg_to_pag

import numpy as np
import subprocess

def gen(n):
    for i in np.arange(n):
        subprocess.run(["Rscript", "R/generate_input.R", f"{i:04}"])

def run(n, keep_skeleton=True):
    for i in np.arange(n):
        bccd = bccd_result(i)
        mag = main(bccd, lst(i), keep_skeleton)
        write_mag_as_pcalg(mag, f"data/{i:04}_mag.csv")
        subprocess.run(["Rscript", "R/mag_to_pag.R", f"{i:04}"])

def compare_results(n):
    results = np.array([
        [compare(bccd_result(i), original_pag(i)),
         compare(result_pag(i), original_pag(i))]
        for i in np.arange(n) ])

    # avg = results.mean(axis=1)
    return results

def give_mean(n):
    x = compare_results(n)
    c = np.isnan(x).any(axis=(1, 2))
    return x[~c].mean(axis=0)

def all(n):
    gen(n)
    run(n)

def bccd_result(n):
    return read_pag(f"data/{n:04}_bccd_result.csv")

def original_pag(n):
    g = read_pag(f"data/{n:04}_original_pag.csv")
    return pcalg_to_pag(g)

def result_pag(n):
    g = read_pag(f"data/{n:04}_pag.csv")
    return pcalg_to_pag(g)

def lst(n):
    return read_lst(f"data/{n:04}_lst.csv")
