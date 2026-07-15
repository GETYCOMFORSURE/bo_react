# 1. data + featurization
# Load CSV, inspect columns, one-hot encode the 4 categorical dimensions → X (45 cols), y = yield

"""
featurize.py
Load the BHpredict (BH_CR_numbers) CSV, one-hot encode the 4 categorical
dimensions, and return X (45 cols) and y (yield).
"""

import pandas as pd

DATA_PATH = "BH_CR_numbers.csv"

CATEGORICAL_COLS = [
    "base_number",
    "ligand_number",
    "aryl_halide_number",
    "additive_number",
]

TARGET_COL = "yield"


def load_raw(path: str = DATA_PATH) -> pd.DataFrame:
    """Load the raw CSV, dropping the stray index column."""
    df = pd.read_csv(path)
    df = df.drop(columns=[c for c in df.columns if c.startswith("Unnamed")])
    return df


def inspect(df: pd.DataFrame) -> None:
    print("Shape:", df.shape)
    print("\nColumns:", df.columns.tolist())
    print("\nUnique counts per categorical column:")
    for col in CATEGORICAL_COLS:
        print(f"  {col}: {df[col].nunique()} unique values")
    print("\nYield stats:")
    print(df[TARGET_COL].describe())


def featurize(df: pd.DataFrame):
    """
    One-hot encode the 4 categorical columns (each treated as a discrete
    category, not a numeric scale) and return X, y.
    """
    df = df.dropna(subset=[TARGET_COL]).copy()

    # cast to category dtype so get_dummies treats these as labels, not numbers
    for col in CATEGORICAL_COLS:
        df[col] = df[col].astype("category")

    X = pd.get_dummies(df[CATEGORICAL_COLS], columns=CATEGORICAL_COLS)
    y = df[TARGET_COL].values

    return X, y


if __name__ == "__main__":
    df = load_raw()
    inspect(df)

    X, y = featurize(df)
    print("\nX shape:", X.shape)   # expect (4135, 45)
    print("y shape:", y.shape)     # expect (4135,)
    print("\nX columns:", X.columns.tolist())
