from thesis.new_mag import gen_new_mag
from thesis.score import score
from thesis.data_io import *

def main(mag, lst, max_iter=1000, keep_skeleton=True):
    # mag = pag_to_mag(pag.copy())
    mag = mag.copy()
    new_mag = gen_new_mag(mag, lst, keep_skeleton)
    n = 0

    print(str(score(mag, lst)) + " -> " + str(score(new_mag, lst)))
    while (
            (score(new_mag, lst) < score(mag, lst))
            and (n <= max_iter)
    ):
        mag = new_mag.copy()
        new_mag = gen_new_mag(new_mag, lst, keep_skeleton)
        n += 1
        print(str(score(mag, lst)) + " -> " + str(score(new_mag, lst)))

    return mag, n
