from conversion import pag_to_mag
from new_mag import adjacent_mags
from read_data import read_pag, read_scst
from score import score

PAG_FILE = "../data/pag1.csv"
SCST_FILE = "../data/scst.csv"

def main(pag, scst, max_iter=1000000, delta=0):
    mag = pag_to_mag(pag)

    mags = adjacent_mags(mag)

    # new_mag = new_mag(mag, scst)
    # n = 0

    # while score(new_mag) > score(mag) + delta and n <= max_iter:
        # mag = new_mag # maybe .copy()
        # new_mag = new_mag(new_mag, scst)
        # n += 1

    # return mag2pag(mag)

def new_mag(mag, scst):
    """TODO: implement"""
    return

g = read_pag(PAG_FILE)
scst = read_scst(SCST_FILE)
main(g, scst)
