from thesis.main import main
from thesis.data_io import (
    write_mag_as_pcalg,
    read_pag,
    read_lst)

from pathlib import Path
from multiprocessing import Pool

import subprocess
import numpy as np
import pandas as pd

def full_run():
    model_args = (
        [(5, 0.6, 1), (15, 0.16, 3)]
        + [(10, edge_prob, 2) for edge_prob in [0.2, 0.25, 0.3]]
    )
    models = np.arange(100)
    samples = 2 ** np.arange(7, 18)
    skel = False

    pool = Pool(7)

    args_gen = [(n, p, m, model) for model in models for n, p, m in
                model_args]
    pool.starmap(gen, args_gen)

    agrs_bccd = [(n, p, m, model, samples) for model in models for n, p, m in
                 model_args]
    pool.starmap(bccd, agrs_bccd)

    # we must complete a full run per model_arg before we do anything in
    # parallel because of how erroneous bccd_mags are handled in run (see
    # while .. == "")
    args_run = [(n, p, m, model, samples, (0.5, 1), skel) for model in
                models for n, p, m in model_args]
    pool.starmap(run, args_run)

    args_diff_prob_run = [
        (10, 0.3, 2, model, samples, (min_prob, 1), skel) for model in models
        for min_prob in [0, 0.00001, 0.01, 0.1, 0.7, 0.9]
    ]

    pool.starmap(run, args_diff_prob_run)

    pool.close()
    pool.join()

def gen(nodes, edge_prob, max_hidden, i, keep_file=True):
    p = Path(f"data/{nodes}_{edge_prob}_{max_hidden}/{i:03}/dag.csv")
    if not p.is_file() or not keep_file:
        p.parent.mkdir(parents = True, exist_ok = True)
        subprocess.run([
            "Rscript",
            "R/gen_graph.R",
            str(max_hidden),
            str(edge_prob),
            str(nodes),
            f"data/{nodes}_{edge_prob}_{max_hidden}/{i:03}/lv.csv",
            f"data/{nodes}_{edge_prob}_{max_hidden}/{i:03}/dag.csv",
            f"data/{nodes}_{edge_prob}_{max_hidden}/{i:03}/pag.csv"
        ])

def bccd(nodes, edge_prob, max_hidden, i, n, keep_file=True):
    for j in n:
        if not Path(f"data/{nodes}_{edge_prob}_{max_hidden}/{i:03}/{j:07}_bpag.csv").is_file() or not keep_file:
            subprocess.run([
                "Rscript",
                "R/run_bccd.R",
                f"{j:07}",
                f"data/{nodes}_{edge_prob}_{max_hidden}/{i:03}/lv.csv",
                f"data/{nodes}_{edge_prob}_{max_hidden}/{i:03}/dag.csv",
                f"data/{nodes}_{edge_prob}_{max_hidden}/{i:03}/{j:07}_cor.csv",
                f"data/{nodes}_{edge_prob}_{max_hidden}/{i:03}/{j:07}_bccd.csv",
                f"data/{nodes}_{edge_prob}_{max_hidden}/{i:03}/{j:07}_lst.csv",
            ],)

            bccd_location = f"data/{nodes}_{edge_prob}_{max_hidden}/{i:03}/{j:07}_bccd.csv"
            bmag_location = f"data/{nodes}_{edge_prob}_{max_hidden}/{i:03}/{j:07}_bmag.csv"
            bpag_location = f"data/{nodes}_{edge_prob}_{max_hidden}/{i:03}/{j:07}_bpag.csv"

            pag_to_mag(bccd_location, bmag_location)
            mag_to_pag(bmag_location, bpag_location)

def run(nodes, edge_prob, max_hidden, i, n, prob_interval, keep_skeleton, keep_file=True):
    for j in n:
        iter_location = f"data/{prob_interval}/{keep_skeleton}/{nodes}_{edge_prob}_{max_hidden}/{i:03}/{j:07}_iter.csv"
        mag_location = f"data/{prob_interval}/{keep_skeleton}/{nodes}_{edge_prob}_{max_hidden}/{i:03}/{j:07}_mag.csv"
        pag_location = f"data/{prob_interval}/{keep_skeleton}/{nodes}_{edge_prob}_{max_hidden}/{i:03}/{j:07}_pag.csv"
        bmag_location = f"data/{nodes}_{edge_prob}_{max_hidden}/{i:03}/{j:07}_bmag.csv"
        lst_location = f"data/{nodes}_{edge_prob}_{max_hidden}/{i:03}/{j:07}_lst.csv"

        if not Path(pag_location).is_file() or not keep_file:
            # if mag is empty we must generate new model and re-do
            # bccd and run on that part
            while Path(bmag_location).read_text() == '':
                # we save the error
                bccd_loc = Path(f"data/{nodes}_{edge_prob}_{max_hidden}/{i:03}/{j:07}_bccd.csv")
                df = pd.read_csv(bccd_loc, header=None)

                error_loc = Path(f"data/errors/{nodes}_{edge_prob}_{max_hidden}_{i:03}_{j:07}_bccd.csv")
                error_loc.parent.mkdir(parents = True, exist_ok = True)
                df.to_csv(error_loc, header=False, index=False)

                print(f"regenerating {nodes}_{edge_prob}_{max_hidden}/{i}")
                gen(nodes, edge_prob, max_hidden, i, keep_file=False)
                bccd(nodes, edge_prob, max_hidden, i, n, keep_file=False)
                run(nodes, edge_prob, max_hidden, i, n,
                    prob_interval, keep_skeleton, keep_file=False)
            # make parent folder
            Path(pag_location).parent.mkdir(parents = True, exist_ok = True)

            bmag = read_pag(bmag_location)
            lst = read_lst(lst_location, prob_interval)
            mag, iterations = main(bmag, lst, keep_skeleton=keep_skeleton)

            # save the number of iterations
            pd.Series(iterations).to_csv(iter_location, header=False, index=False)

            write_mag_as_pcalg(mag, mag_location)
            mag_to_pag(mag_location, pag_location)

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
