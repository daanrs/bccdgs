from conversion import pag_to_mag
from new_mag import new_mag
from read_data import read_pag, read_scst
from score import score

PAG_FILE = "../data/pag2.csv"
SCST_FILE = "../data/scst.csv"

# TODO: this is all pseudocode
def main(pag, scst, max_iter=1000000, delta=0):
    mag = pag2mag(pag)

    new_mag = new_mag(mag, scst)
    n = 0

    while score(new_mag) > score(mag) + delta and n <= max_iter:
        mag = new_mag # maybe .copy()
        new_mag = new_mag(new_mag, scst)
        n += 1

    return mag2pag(mag)

pag = read_pag(PAG_FILE)

print("Pag:")
print(pag)

pag_to_mag(pag)
