from thesis.new_mag import gen_new_mag
from thesis.score import score, score_dict
from thesis.conversion import mag_to_ancestral

def bccdgs(mag, lst, n, k, min_prob, max_iter=1000):
    sts = score_dict(lst, min_prob)

    mag = mag.copy()
    mag_tc = mag_to_ancestral(mag)
    mag_score = score(mag, mag_tc, **sts)

    new_mag = gen_new_mag(mag, sts, n, k)
    new_mag_tc = mag_to_ancestral(new_mag)
    new_mag_score = score(new_mag, new_mag_tc, **sts)
    it = 0

    while (new_mag_score > mag_score) and (it <= max_iter):
        print(f"{mag_score} -> {new_mag_score}")
        mag = new_mag.copy()
        mag_tc = new_mag_tc
        mag_score = new_mag_score

        new_mag = gen_new_mag(mag, sts, n, k)
        new_mag_tc = mag_to_ancestral(new_mag)
        new_mag_score = score(new_mag, new_mag_tc, **sts)
        it += 1

    return mag, it
