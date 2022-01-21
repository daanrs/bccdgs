from thesis.main import main
from thesis.data_io import bccd_result, lst, original_pag, result_pag
from thesis.compare import show_comparison

import subprocess

subprocess.run(["Rscript", "R/generate_input.R"])

bccd = bccd_result()
main(bccd, lst())

subprocess.run(["Rscript", "R/mag_to_pag.R"])

og = original_pag()
g = result_pag()

print("bccd: " + show_comparison(bccd, og))
print("result: " + show_comparison(og, g))
