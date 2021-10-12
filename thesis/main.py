from conversion import pag2mag, mag2pag
from new_mag import new_mag
from score import score

def main(pag, scst, max_iter=1000000, delta=0):
    mag = pag2mag(pag)

    new_mag = new_mag(mag, scst)
    n = 0

    while score(new_mag) > score(mag) + delta and n <= max_iter:
        mag = new_mag # maybe .copy()
        new_mag = new_mag(new_mag, scst)
        n += 1

    return mag2pag(mag)
