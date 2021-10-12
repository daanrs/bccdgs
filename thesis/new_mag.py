def new_mag(mag, scst):
    return max(adjacent_mags(mag), key=lambda x: score(x, scst))

def adjacent_mags(mag):
    return [mag]

