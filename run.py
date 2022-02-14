from thesis.main import main
from thesis.data_io import (
    write_mag_as_pcalg,
    read_pag,
    read_lst,
    gen_loc,
    bccd_loc,
    run_loc
)

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

    # generate models
    for model in models:
        for n, p, m in model_args:
            gen(n, p, m, model)

    # we run bccd in parallel, since that can take a while
    pool = Pool(4)
    agrs_bccd = [(n, p, m, model, samples) for model in models for n, p, m in
                 model_args]
    pool.starmap(bccd, agrs_bccd)
    pool.close()
    pool.join()

    # run code
    for model in models:
        for n, p, m in model_args:
            run(n, p, m, model, samples, (0.5, 1), skel)
        run(10, 0.25, 2, model, samples, (0.5, 1), True)

    for model in np.arange(50):
        for min_prob in [0, 0.001, 0.1, 0.7, 0.9]:
            run(10, 0.25, 2, model, samples, (min_prob, 1), skel)

def gen(nodes, edge_prob, max_hidden, i, keep_file=True):
    p = Path(gen_loc(nodes, edge_prob, max_hidden, i) + "dag.csv")
    if not p.is_file() or not keep_file:
        print(f"Generating {i}")

        p.parent.mkdir(parents = True, exist_ok = True)
        subprocess.run([
            "Rscript",
            "R/gen_graph.R",
            str(max_hidden),
            str(edge_prob),
            str(nodes),
            gen_loc(nodes, edge_prob, max_hidden, i) + "lv.csv",
            gen_loc(nodes, edge_prob, max_hidden, i) + "dag.csv",
            gen_loc(nodes, edge_prob, max_hidden, i) + "pag.csv"
        ])

def bccd(nodes, edge_prob, max_hidden, i, n, keep_file=True):
    for j in n:
        if not Path(bccd_loc(nodes, edge_prob, max_hidden, i, j) + "bpag.csv").is_file() or not keep_file:
            subprocess.run([
                "Rscript",
                "R/run_bccd.R",
                f"{j:07}",
                gen_loc(nodes, edge_prob, max_hidden, i) + "lv.csv",
                gen_loc(nodes, edge_prob, max_hidden, i) + "dag.csv",
                bccd_loc(nodes, edge_prob, max_hidden, i, j) + "cor.csv",
                bccd_loc(nodes, edge_prob, max_hidden, i, j) + "bccd.csv",
                bccd_loc(nodes, edge_prob, max_hidden, i, j) + "lst.csv",
            ],)

            bccd_location = bccd_loc(nodes, edge_prob, max_hidden, i, j) + "bccd.csv"
            bmag_location = bccd_loc(nodes, edge_prob, max_hidden, i, j) + "bmag.csv"
            bpag_location = bccd_loc(nodes, edge_prob, max_hidden, i, j) + "bpag.csv"

            pag_to_mag(bccd_location, bmag_location)
            mag_to_pag(bmag_location, bpag_location)

def run(nodes, edge_prob, max_hidden, i, n, prob_interval, keep_skeleton, keep_file=True):
    for j in n:
        output_loc = run_loc(nodes,
                             edge_prob, max_hidden, i, j,
                             prob_interval, keep_skeleton)
        iter_location = output_loc + "iter.csv"
        mag_location = output_loc + "mag.csv"
        pag_location = output_loc + "pag.csv"

        bccd_location = bccd_loc(nodes, edge_prob, max_hidden, i, j) + "bccd.csv"
        bmag_location = bccd_loc(nodes, edge_prob, max_hidden, i, j) + "bmag.csv"
        lst_location = bccd_loc(nodes, edge_prob, max_hidden, i, j) + "lst.csv"

        if not Path(pag_location).is_file() or not keep_file:
            # if mag is empty we must generate new model and re-do
            # bccd and run on that part
            while Path(bmag_location).read_text() == '':
                # we save the error
                df = pd.read_csv(bccd_location, header=None)

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

            print(f"Run  {nodes}, {edge_prob}, {keep_skeleton}, {prob_interval}: {i}, {j}")
            mag, iterations = main(bmag, lst, keep_skeleton=keep_skeleton)
            print(f"Done {nodes}, {edge_prob}, {keep_skeleton}, {prob_interval}: {i}, {j}, n = {iterations}")

            # save the number of iterations
            pd.Series([iterations]).to_csv(iter_location, header=False, index=False)

            # save the mag and turn it into a pag
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
