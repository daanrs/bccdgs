import pandas as pd

from pathlib import Path

data = Path("./data")

df = pd.concat(
    [pd.read_pickle(p) for p in data.glob("**/bccdgs_score.pkl")]
)
