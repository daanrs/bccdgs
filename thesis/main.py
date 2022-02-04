from thesis.new_mag import gen_new_mag
from thesis.score import score

def main(mag, lst, keep_skeleton, max_iter=1000):
    mag = mag.copy()
    new_mag = gen_new_mag(mag, lst, keep_skeleton)
    n = 0

    while (
            (score(new_mag, lst) > score(mag, lst))
            and (n <= max_iter)
    ):
        mag = new_mag.copy()
        new_mag = gen_new_mag(new_mag, lst, keep_skeleton)
        n += 1

    return mag, n
