"""
predictor.py
------------
Loads the per-disease models and returns the risk for ONE disease.
No Streamlit code here, so it is easy to test.
"""

import os
import pickle
import pandas as pd

from symptoms import disease_key

MODEL_DIR = os.path.join(os.path.dirname(__file__), "models")


def load_model(disease):
    key = disease_key(disease)
    with open(os.path.join(MODEL_DIR, f"{key}_model.pkl"), "rb") as f:
        model = pickle.load(f)
    with open(os.path.join(MODEL_DIR, f"{key}_features.pkl"), "rb") as f:
        feats = pickle.load(f)
    return model, feats


def risk_level(p):
    if p >= 0.65:
        return "High"
    if p >= 0.35:
        return "Moderate"
    return "Low"


def predict(disease, age, yes_symptoms, loaded=None):
    """Returns (probability 0-1 of this disease, risk level text)."""
    model, feats = loaded or load_model(disease)
    chosen = set(yes_symptoms)
    row = {"age": age, **{f: int(f in chosen) for f in feats if f != "age"}}
    X = pd.DataFrame([row])[feats]
    p = float(model.predict_proba(X)[0][list(model.classes_).index(1)])
    return p, risk_level(p)
