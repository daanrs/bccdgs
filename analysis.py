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

df25 = df[df["degree"] == 2.5]

# NODES
df_nodes = df[(df["degree"] == 2.5) & (~df["skeleton"]) & (df["k"] <= 1)]
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

# SPARSITY
df_sparsity = df[
    (np.isin(df["degree"], np.array([2, 2.5, 3])))
    & (df["nodes"] == 10)
    & (~df["skeleton"])
    & (df["k"] <= 1)
]

g = sns.relplot(
    data=df_sparsity, x="samples", y="pag_acc", kind="line", hue="pagtype",
    col="degree"
)
g.axes[0, 0].set_xscale("log", base=10)
g.savefig(output / "sparsity_pag.pdf")

g = sns.relplot(
    data=df_sparsity, x="samples", y="causal_acc", kind="line", hue="pagtype",
    col="degree"
)
g.axes[0, 0].set_xscale("log", base=10)
g.savefig(output / "sparsity_causal.pdf")

# SKEL
df_skel = df25[(df25["nodes"] == 10) & (df25["pagtype"] == "bccdgs")]

g = sns.relplot(
    data=df_skel, x="samples", y="pag_acc", kind="line",
    hue=df_skel[["k", "skeleton"]].apply(tuple, axis=1)
)
g.axes[0, 0].set_xscale("log", base=10)
g.savefig(output / "skel_pag.pdf")

g = sns.relplot(
    data=df_skel, x="samples", y="pag_acc", kind="line",
    hue=df_skel[["k", "skeleton"]].apply(tuple, axis=1)
)
g.axes[0, 0].set_xscale("log", base=10)
g.savefig(output / "skel_causal.pdf")
