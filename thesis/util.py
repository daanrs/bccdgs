import numpy as np

def choices(n, k):
    if k == 1:
        return n.reshape(n.shape[:1] + (1,) + n.shape[1:])
    n_k = np.array([])
    for i in range(n.shape[0]-k+1):
        n_k_1 = choices(n[i+1:], k-1)
        x = np.tile(n[i],
                    n_k_1.shape[:1]
                    + tuple(np.repeat(1, len(n_k_1.shape) -1)))
        x_k = np.concatenate((x, n_k_1), axis=1)
        if n_k.size == 0:
            n_k = x_k
        else:
            n_k = np.concatenate((n_k, x_k))

    return n_k
