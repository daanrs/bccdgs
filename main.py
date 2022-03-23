import numpy as np

from thesis.run import run

def main():
    run(
        nodes = 5,
        edge_prob = 0.6,
        max_hidden_nodes = 1,
        models = np.arange(100),
        samples = 2 ** np.arange(7, 18),
        min_prob = 0.5,
        skel = False,
        seed = 5,
        write = True
    )

    run(
        nodes = 10,
        edge_prob = 0.3,
        max_hidden_nodes = 2,
        models = np.arange(100),
        samples = 2 ** np.arange(7, 18),
        min_prob = 0.5,
        skel = False,
        seed = 5,
        write = True
    )

    run(
        nodes = 15,
        edge_prob = 0.16,
        max_hidden_nodes = 3,
        models = np.arange(100),
        samples = 2 ** np.arange(7, 18),
        min_prob = 0.5,
        skel = False,
        seed = 5,
        write = True
    )

    run(
        nodes = 10,
        edge_prob = 0.4,
        max_hidden_nodes = 2,
        models = np.arange(100),
        samples = 2 ** np.arange(7, 18),
        min_prob = 0.5,
        skel = False,
        seed = 5,
        write = True
    )

    for p in [0, 0.01, 0.1, 0.3, 0.5, 0.7, 0.9]:
        run(
            nodes = 10,
            edge_prob = 0.4,
            max_hidden_nodes = 2,
            models = np.arange(100),
            samples = 2 ** np.arange(7, 18),
            min_prob = p,
            skel = False,
            seed = 5,
            write = True
        )

if __name__ == "__main__":
    main()
