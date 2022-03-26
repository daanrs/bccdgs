# type: ignore

import numpy as np
import pandas as pd

from pathlib import Path

from bccdgs.run import (
    gen_data,
    bccd_df,
    mag_df,
    bccdgs_df,
    pag_df,
    pag_score_df
)

def main(data_loc, mdf_loc, bdf_loc, pdf_loc, psdf_loc, overwrite):
    if (not data_loc.exists()) or overwrite:
        # df_10 = pd.concat(
            # [
                # gen_data(
                    # nodes = 10,
                    # degree = d,
                    # max_hidden_nodes = 2,
                    # models = np.arange(100),
                    # samples = 2 ** np.arange(7, 18),
                    # seed = 5,
                # )
                # for d in [2, 3, 4]
            # ]
        # )

        # df_5_15 = pd.concat((
            # gen_data(
                # nodes = 5,
                # degree = 3,
                # max_hidden_nodes = 1,
                # models = np.arange(100),
                # samples = 2 ** np.arange(7, 18),
                # seed = 5,
            # ),
            # gen_data(
                # nodes = 15,
                # degree = 3,
                # max_hidden_nodes = 3,
                # models = np.arange(100),
                # samples = 2 ** np.arange(7, 18),
                # seed = 5,
            # )
        # ))
        # df = pd.concat((df_5_15, df_10))

        df = bccd_df(gen_data(
            nodes = 10,
            degree = 3,
            max_hidden_nodes = 2,
            models = np.arange(100),
            samples = [4096],
            seed = 5,
        ))

        # df = bccd_df(gen_data(models=range(2)))

        df.to_pickle(data_loc)
    else:
        df = pd.read_pickle(data_loc)

    selection_bias = df["pag"].apply(
        lambda g: ((g == 1) & (g.T == 1)).any()
    )
    df = df[~selection_bias]

    if not mdf_loc.exists() or overwrite:
        mdf = mag_df(df)
        mdf.to_pickle(mdf_loc)
    else:
        mdf = pd.read_pickle(mdf_loc)

    no_valid_mag = mdf["mag"].isna()
    mdf = mdf[~no_valid_mag]
    df = df[~no_valid_mag]

    if not bdf_loc.exists() or overwrite:
        bdf = pd.concat([
            bccdgs_df(mdf, 1, k, skel, p)
            for k in [1, 2]
            for skel in [True, False]
            for p in [0, 0.1, 0.3, 0.5, 0.7, 0.9]
            # for p in [0.5]
        ])
        bdf.to_pickle(bdf_loc)
    else:
        bdf = pd.read_pickle(bdf_loc)

    mbdf = pd.concat((mdf, bdf))

    if not pdf_loc.exists() or overwrite:
        pdf = pd.concat((
            pag_df(mbdf), df
        ))
        pdf.to_pickle(pdf_loc)
    else:
        pdf = pd.read_pickle(pdf_loc)

    if not psdf_loc.exists() or overwrite:
        psdf = pag_score_df(pdf)
        psdf.to_pickle(psdf_loc)

if __name__ == "__main__":
    loc = Path("data")
    main(
        loc / "data.pkl",
        loc / "mdf.pkl",
        loc / "bdf.pkl",
        loc / "pdf.pkl",
        loc / "psdf.pkl",
        True
    )
