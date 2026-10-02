"""
train_models.py
----------------
Trains ONE Random Forest per disease (5 models). Each model looks only at
age + the symptoms asked on that disease's page and answers:
"how likely is THIS disease?"  (disease vs everything else)

Saves into models/:
    <key>_model.pkl      e.g. diabetes_model.pkl, heart_model.pkl ...
    <key>_features.pkl   exact feature order for that model

Run:
    python data_generator.py
    python train_models.py
"""

import os
import pickle
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

from symptoms import DISEASES, disease_features, disease_key

BASE = os.path.dirname(__file__)
DATA_PATH = os.path.join(BASE, "data", "symptoms.csv")
MODEL_DIR = os.path.join(BASE, "models")


def train_one(df, disease):
    feats = disease_features(disease)
    X = df[feats]
    y = (df["disease"] == disease).astype(int)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    clf = RandomForestClassifier(
        n_estimators=300, min_samples_leaf=3, class_weight="balanced",
        random_state=42, n_jobs=-1,
    )
    clf.fit(X_train, y_train)

    preds = clf.predict(X_test)
    acc = accuracy_score(y_test, preds)
    print(f"\n=== {disease.upper()} ===  ({len(feats) - 1} symptoms + age)")
    print(f"Test accuracy: {acc * 100:.2f}%")
    print(classification_report(y_test, preds, target_names=["Other", disease]))

    key = disease_key(disease)
    with open(os.path.join(MODEL_DIR, f"{key}_model.pkl"), "wb") as f:
        pickle.dump(clf, f)
    with open(os.path.join(MODEL_DIR, f"{key}_features.pkl"), "wb") as f:
        pickle.dump(feats, f)
    return acc


def main():
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError("data/symptoms.csv not found. Run `python data_generator.py` first.")
    os.makedirs(MODEL_DIR, exist_ok=True)
    df = pd.read_csv(DATA_PATH).dropna()

    results = {d: train_one(df, d) for d in DISEASES}
    print("\n================ SUMMARY ================")
    for d, acc in results.items():
        print(f"{d:22s}: {acc * 100:.2f}% accuracy")
    print("All models saved in the models/ folder.")


if __name__ == "__main__":
    main()
