import numpy as np

def choices(n, k):
    """
    All k choose n combinations.
    """
    if (k < 1) or (k > len(n)):
        raise ValueError("We must have 1 <= k <= len(n)")
    elif k == 1:
        return n.reshape(n.shape[:1] + (1,) + n.shape[1:])
    else:
        return np.concatenate(
            [
                np.concatenate(
                    (
                        n_k_1 := choices(n[i+1:], k-1),
                        np.broadcast_to(
                            n[i],
                            (n_k_1.shape[0], 1) + n[i].shape
                        )
                    ),
                    axis = 1
                )
                for i in range(n.shape[0]-k+1)
            ]
        )

def product_align(x, y):
    """
    Repeat x and y in such a way that concatenating x and y would return
    their product.

    Given x.shape = (x1, x2, ..., xn)
    and y.shape = (y1, y2, ..., yn)
    return xs and ys with shape (x1 * y1, x2, ...) (x1 * y1, y2, ...)
    """
    x_prod_dim = x.shape[0]
    y_prod_dim = y.shape[0]
    xs = np.broadcast_to(x, (y_prod_dim,) + (x.shape))
    ys = np.broadcast_to(y, (x_prod_dim,) + (y.shape))

    xs = np.reshape(
        xs,
        (x_prod_dim * y_prod_dim,) + (x.shape[1:]),
        order='F'
    )
    ys = np.reshape(
        ys,
        (x_prod_dim * y_prod_dim,) + (y.shape[1:]),
        order='C'
    )
    return xs, ys
