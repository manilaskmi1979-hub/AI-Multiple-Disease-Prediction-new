"""
data_generator.py
------------------
Generates a SYNTHETIC symptom dataset (data/symptoms.csv) for:
    Diabetes, Heart Disease, Liver Disease, Kidney Disease, Parkinson's Disease
    + "No Major Concern"

Each row = one person: age + Yes(1)/No(0) for every symptom in symptoms.py.
Symptom probabilities per disease come from symptoms.py (PROFILES), based on
commonly described symptoms. A per-person "severity" factor makes some people
mild (few symptoms) so the model does not become over-confident.

NOTE: This is synthetic, for learning / demo. For a real project, replace it
with a labelled clinical symptom dataset (e.g. a Kaggle "disease symptom
prediction" dataset) using the same layout: columns = age + symptom columns
+ a "disease" column.
"""

import os
import numpy as np
import pandas as pd
from symptoms import SYMPTOM_IDS, PROFILES, BASELINE, DEFAULT_BASE, AGE_RANGE, CLASSES, NONE_LABEL

SEED = 42
OUT_DIR = os.path.join(os.path.dirname(__file__), "data")


def make_rows(label, n, rng):
    profile = PROFILES.get(label, {})
    lo, hi = AGE_RANGE[label]
    rows = []
    for _ in range(n):
        # mild / moderate / severe person
        severity = rng.uniform(0.55, 1.0) if label != NONE_LABEL else 1.0
        row = {"age": int(rng.integers(lo, hi + 1))}
        for sid in SYMPTOM_IDS:
            base = BASELINE.get(sid, DEFAULT_BASE)
            p = profile[sid] * severity if sid in profile else base
            row[sid] = int(rng.random() < max(p, base))
        row["disease"] = label
        rows.append(row)
    return rows


def main(n_per_class=700):
    rng = np.random.default_rng(SEED)
    rows = []
    for label in CLASSES:
        n = n_per_class + (300 if label == NONE_LABEL else 0)   # more healthy examples
        rows += make_rows(label, n, rng)
    df = pd.DataFrame(rows).sample(frac=1, random_state=SEED).reset_index(drop=True)
    os.makedirs(OUT_DIR, exist_ok=True)
    path = os.path.join(OUT_DIR, "symptoms.csv")
    df.to_csv(path, index=False)
    print(f"Saved {path}  shape={df.shape}")
    print(df["disease"].value_counts())


if __name__ == "__main__":
    main()
