from pathlib import Path

import numpy as np
import pandas as pd
import seaborn as sns

sns.set_theme()

data = Path("./data")
output = Path("./report/lib")

df = pd.concat(
    [pd.read_pickle(p) for p in data.glob("**/bccdgs_score.pkl")]
)

df = df.fillna(
    value={
        "k": 0,
        "skeleton": False,
        "min_prob": -1,
        "it": 0
    },
    axis=0
)

df = df.reset_index(drop=True)

# NODES
df_nodes = df[
    (df["degree"] == 2.5)
    & (~df["skeleton"])
    & (df["k"] <= 1)
    & ((df["min_prob"] == 0.5) | (df["min_prob"] == -1))
]
g = sns.relplot(
    data=df_nodes, x="samples", y="pag_acc", kind="line", hue="pagtype",
    col="nodes"
)
g.axes[0, 0].set_xscale("log", base=10)
g.savefig(output / "nodes_pag.pdf")

g = sns.relplot(
    data=df_nodes, x="samples", y="causal_acc", kind="line", hue="pagtype",
    col="nodes"
)
g.axes[0, 0].set_xscale("log", base=10)
g.savefig(output / "nodes_causal.pdf")
print("nodes done")

# density
df_density = df[
    (np.isin(df["degree"], np.array([2, 2.5, 3])))
    & (df["nodes"] == 10)
    & (~df["skeleton"])
    & (df["k"] <= 1)
    & ((df["min_prob"] == 0.5) | (df["min_prob"] == -1))
]

g = sns.relplot(
    data=df_density, x="samples", y="pag_acc", kind="line", hue="pagtype",
    col="degree"
)
g.axes[0, 0].set_xscale("log", base=10)
g.savefig(output / "density_pag.pdf")

g = sns.relplot(
    data=df_density, x="samples", y="causal_acc", kind="line", hue="pagtype",
    col="degree"
)
g.axes[0, 0].set_xscale("log", base=10)
g.savefig(output / "density_causal.pdf")
print("density done")

# SKEL
df_skel_k = df[
    (df["nodes"] == 10)
    & (df["degree"] == 2.5)
    & (df["pagtype"] == "bccdgs")
    & ((df["min_prob"] == 0.5) | (df["min_prob"] == -1))
]

df_skel = df_skel_k[df_skel_k["k"] == 1]
df_k = df_skel_k[~df_skel_k["skeleton"]]

g = sns.relplot(
    data=df_k, x="samples", y="pag_acc", kind="line",
    hue="k",
    palette="tab10"
)
g.axes[0, 0].set_xscale("log", base=10)
g.savefig(output / "k_pag.pdf")

g = sns.relplot(
    data=df_k, x="samples", y="causal_acc", kind="line",
    hue="k",
    palette="tab10"
)
g.axes[0, 0].set_xscale("log", base=10)
g.savefig(output / "k_causal.pdf")

g = sns.relplot(
    data=df_skel, x="samples", y="pag_acc", kind="line",
    hue="skeleton",
    palette="tab10",
)
g.axes[0, 0].set_xscale("log", base=10)
g.savefig(output / "skel_pag.pdf")

g = sns.relplot(
    data=df_skel, x="samples", y="causal_acc", kind="line",
    hue="skeleton",
    palette="tab10",
)
g.axes[0, 0].set_xscale("log", base=10)
g.savefig(output / "skel_causal.pdf")

g = sns.relplot(
    data=df_skel_k, x="samples", y="pag_acc", kind="line",
    hue=df_skel_k[["k", "skeleton"]].apply(tuple, axis=1),
    palette="tab10",
)
g.axes[0, 0].set_xscale("log", base=10)
g.savefig(output / "skel_k_pag.pdf")

g = sns.relplot(
    data=df_skel_k, x="samples", y="causal_acc", kind="line",
    hue=df_skel_k[["k", "skeleton"]].apply(tuple, axis=1),
    palette="tab10",
)
g.axes[0, 0].set_xscale("log", base=10)
g.savefig(output / "skel_k_causal.pdf")
print("skeleton done")

# CUTOFF
df_cutoff = df[
    (df["nodes"] == 10)
    & (df["degree"] == 2.5)
    & (df["pagtype"] == "bccdgs")
    & (~df["skeleton"])
    & (df["k"] <= 1)
    & (
        (df["min_prob"] == 0)
        | (df["min_prob"] == 0.1)
        | (df["min_prob"] == 0.3)
        | (df["min_prob"] == 0.5)
        | (df["min_prob"] == 0.7)
        | (df["min_prob"] == 0.9)
    )
]

g = sns.relplot(
    data=df_cutoff, x="samples", y="pag_acc", kind="line", hue="min_prob",
    palette="tab10",
    # col=(df_cutoff["min_prob"] < 0.5)
)
g.axes[0, 0].set_xscale("log", base=10)
g.savefig(output / "cutoff_pag.pdf")

g = sns.relplot(
    data=df_cutoff, x="samples", y="causal_acc", kind="line", hue="min_prob",
    palette="tab10",
    # col=(df_cutoff["min_prob"] < 0.5)
)
g.axes[0, 0].set_xscale("log", base=10)
g.savefig(output / "cutoff_causal.pdf")
print("cutoff done")
