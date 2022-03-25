# type: ignore

# import numpy as np
import pandas as pd

from thesis.run import (
    gen_data,
    mag_df,
    bccdgs_df,
    pag_df,
    pag_score_df
)

def main():
    df_10 = pd.concat(
        [
            gen_data(
                nodes = 10,
                degree = d,
                max_hidden_nodes = 2,
                models = np.arange(100),
                samples = 2 ** np.arange(7, 18),
                seed = 5,
            )
            for d in [2, 3, 4]
        ]
    )

    df_5_15 = pd.concat((
        gen_data(
            nodes = 5,
            degree = 3,
            max_hidden_nodes = 1,
            models = np.arange(100),
            samples = 2 ** np.arange(7, 18),
            seed = 5,
        ),
        gen_data(
            nodes = 15,
            degree = 3,
            max_hidden_nodes = 3,
            models = np.arange(100),
            samples = 2 ** np.arange(7, 18),
            seed = 5,
        )
    ))

    df = pd.concat((df_5_15, df_10))
    # df = gen_data(models=range(2))
    df.to_pickle("data/data_df.pkl")

    mdf = mag_df(df)
    bdf = pd.concat([
        bccdgs_df(mdf, 1, k, p)
        for k in [1, 2]
        for p in [0.5]
    ])

    mdf = pd.concat((mdf, bdf))
    mdf.to_pickle("data/mag_df.pkl")

    pdf = pd.concat((
        pag_df(mdf), df
    ))
    pdf.to_pickle("data/pag_df.pkl")

    psdf = pag_score_df(pdf)
    psdf.to_pickle("data/pag_score_df.pkl")


if __name__ == "__main__":
    main()
