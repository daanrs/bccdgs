
import pandas as pd

from pathlib import Path

from bccdgs.run import (
    gen_df,
    mag_df,
    bccdgs_df,
    pag_df,
    pag_score_df
)


def bccdgs_generate(nodes,
                    degree,
                    max_latent_variables,
                    location=Path("data"),
                    ):

    location = location / f"{nodes}_{degree}"
    location.mkdir()

    df = gen_df(
        nodes=nodes,
        degree=degree,
        max_latent_variables=max_latent_variables
    )
    df.to_pickle(location / "data_full.pkl")

    mdf = mag_df(df)
    mdf.to_pickle(location / "mag_full.pkl")

    no_valid_mag = mdf["mag"].isna()
    mdf = mdf[~no_valid_mag]
    df = df[~no_valid_mag]

    df.to_pickle(location / "data_valid.pkl")
    mdf.to_pickle(location / "mag_valid.pkl")


def bccdgs_run(nodes,
               degree,
               k,
               skeleton,
               min_prob,
               location=Path("data"),
               ):

    location = location / f"{nodes}_{degree}"
    if not location.exists():
        raise ValueError("data does not exist")

    mdf = pd.read_pickle(location / "mag_valid.pkl")
    df = pd.read_pickle(location / "data_valid.pkl")

    location = location / f"{k}_{skeleton}_{min_prob}"
    location.mkdir()

    bdf = bccdgs_df(mdf, k, skeleton, min_prob)

    mbdf = pd.concat((mdf, bdf))
    mbdf.to_pickle(location / "bccdgs_mag.pkl")

    pdf = pd.concat((
        pag_df(mbdf), df
    ))
    pdf.to_pickle(location / "bccdgs_pag.pkl")

    psdf = pag_score_df(pdf)
    psdf.to_pickle(location / "bccdgs_score.pkl")


def main():

    for d in [2, 2.5, 3]:
        bccdgs_generate(
            nodes=10,
            degree=d,
            max_latent_variables=2,
        )

    bccdgs_generate(
        nodes=5,
        degree=2.5,
        max_latent_variables=1
    )

    bccdgs_generate(
        nodes=15,
        degree=2.5,
        max_latent_variables=3
    )

    for s in [True, False]:
        for k in [1, 2]:
            bccdgs_run(
                nodes=10,
                degree=2.5,
                k=k,
                skeleton=s,
                min_prob=0.5
            )

    for d in [2, 3]:
        bccdgs_run(
            nodes=10,
            degree=d,
            k=1,
            skeleton=False,
            min_prob=0.5
        )

    bccdgs_run(
        nodes=5,
        degree=2.5,
        k=1,
        skeleton=False,
        min_prob=0.5
    )

    bccdgs_run(
        nodes=15,
        degree=2.5,
        k=1,
        skeleton=False,
        min_prob=0.5
    )

    for m in [0, 0.01, 0.1, 0.3, 0.7, 0.9]:
        bccdgs_run(
            nodes=10,
            degree=2.5,
            k=1,
            skeleton=False,
            min_prob=m
        )


if __name__ == "__main__":
    main()
