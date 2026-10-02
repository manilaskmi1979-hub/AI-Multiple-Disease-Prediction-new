# AI-Based Multiple Disease Prediction
**Predicting Health, Protecting Lives**

A machine learning system that checks the risk of **5 diseases** — Diabetes, Heart Disease,
Liver Disease, Kidney Disease and Parkinson's Disease. The user picks a disease on the Home page,
a **separate page for that disease** opens, and they answer simple **Yes / No symptom questions**
(English + Tamil). No lab values needed. The result is a **Low / Moderate / High** risk.

## 📁 Project Structure
```
├── app.py              # Streamlit web app (Login, Symptom Checker, History, About)
├── theme.py            # Colours, disease icons (SVG), CSS
├── symptoms.py         # Symptom questions (EN + தமிழ்), disease profiles, advice
├── data_generator.py   # Creates the symptom dataset  -> data/symptoms.csv
├── train_models.py     # Trains 5 Random Forests (one per disease) -> models/*.pkl
├── predictor.py        # Loads a disease model + returns probability and risk level
├── db.py               # SQLite: users (name + phone) and prediction history
├── requirements.txt
├── data/               # symptoms.csv
└── models/             # created by train_models.py
```

## ⚙️ Modules
1. **Login** – only *Name* and *Phone number* (10-digit Indian mobile). New numbers are registered automatically.
2. **Home** – 5 colour-coded disease cards. Clicking one opens only that disease's page.
3. **Disease page** (Diabetes / Heart / Liver / Kidney / Parkinson's) – age + 13-14 symptoms, one line each with **Yes / No** buttons.
4. **Prediction** – a separate `RandomForestClassifier` per disease (age + that disease's symptoms) gives the probability → **Low / Moderate / High** risk.
5. **Result & Suggestions** – risk card, doctor to meet, tests to ask for, a tip, and an emergency alert for possible heart-attack symptoms.
6. **History** – every check is saved against the user's phone number.

## 🚀 Setup & Run
```bash
pip install -r requirements.txt
python data_generator.py      # (data/symptoms.csv is already included; run to regenerate)
python train_models.py        # trains and saves models/
streamlit run app.py
```
Opens at `http://localhost:8501`.

## 📝 Dataset note
`data_generator.py` builds **synthetic** data from commonly described symptoms of each disease
(see `PROFILES` in `symptoms.py`). For your final report, mention this clearly, or replace
`data/symptoms.csv` with a real labelled symptom dataset using the same columns
(`age`, one 0/1 column per symptom id, and `disease`), then re-run `python train_models.py`.

## 🔐 Login note
Login uses name + phone only (no OTP/password), as requested. Anyone who knows a phone
number can open that user's history. For public deployment add OTP verification.

## 🔮 Future Enhancements
- Add more diseases and symptoms
- Train on real clinical symptom data / XGBoost / Neural Networks
- OTP-based login
- Mobile application, wearable integration

## ⚠️ Disclaimer
This tool provides only a quick ML-based estimate and is **not** a medical diagnosis.
Always consult a qualified doctor.

---
**Project:** AI-Based Multiple Disease Prediction
**Name:** Priyadharshini B | **Reg No:** C4S27603
**Guide:** Dr. M. Gokiladevi, MCA., B.Ed., M.Phil., Ph.D.
