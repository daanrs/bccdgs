import numpy as np

from thesis.run import gen_data

def main():
    gen_data(
        nodes = 5,
        degree = 2,
        max_hidden_nodes = 1,
        models = np.arange(100),
        samples = 2 ** np.arange(7, 18),
        seed = 5,
        write = True
    )

    for d in [2, 2.5, 3]:
        gen_data(
            nodes = 10,
            degree = d,
            max_hidden_nodes = 2,
            models = np.arange(100),
            samples = 2 ** np.arange(7, 18),
            seed = 5,
            write = True
        )

    gen_data(
        nodes = 15,
        degree = 2,
        max_hidden_nodes = 3,
        models = np.arange(100),
        samples = 2 ** np.arange(7, 18),
        seed = 5,
        write = True
    )

if __name__ == "__main__":
    main()
