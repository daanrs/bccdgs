from thesis.main import main
from thesis.data_io import (
    write_mag_as_pcalg,
    read_pag,
    read_lst)

from pathlib import Path

import subprocess

# HIDDEN      = "1"
# PROBABILITY = "0.6"
# NODES       = "5"

HIDDEN      = "2"
PROBABILITY = "0.4"
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
            if not Path(f"data/{NODES}/{i:03}/{j:07}_fci.csv").is_file() or not keep_file:
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
