"""
app.py
------
AI-Based Multiple Disease Prediction - Streamlit web app

Flow:  Login (Name + Phone)  ->  Home (pick a disease)  ->  that disease's page
       (Yes / No symptoms)  ->  Predict  ->  Risk result + advice  ->  History

Run:
    python data_generator.py     # once
    python train_models.py       # once
    streamlit run app.py
"""

import json
import streamlit as st

import db
import predictor
import theme
from symptoms import (
    DISEASES, SYMPTOMS, ADVICE, EMERGENCY_NOTE, disease_symptoms, disease_key, emergency_flag,
)

st.set_page_config(page_title="AI Multiple Disease Prediction", page_icon="🩺", layout="wide")
st.markdown(theme.CSS, unsafe_allow_html=True)
db.init_db()

SYMPTOM_BY_ID = {sid: (en, ta) for sid, en, ta, _ in SYMPTOMS}
DISCLAIMER = ("⚠️ This tool gives only a quick estimate based on the symptoms you answer. "
              "It is NOT a medical diagnosis. Please consult a doctor for confirmation.")
PAGES = ["Home"] + DISEASES + ["My History", "About"]


@st.cache_resource
def get_model(disease):
    return predictor.load_model(disease)


def go_to(page):
    """Button callback: open another page (also updates the sidebar menu)."""
    st.session_state["page"] = page


# ------------------------------------------------------------------ helpers
def qkey(disease, sid):
    return f"sym_{disease_key(disease)}_{sid}"


def question_html(en, ta, lang, color, is_yes):
    if lang == "English":
        text = en
    elif lang == "தமிழ்":
        text = ta
    else:
        text = f"{en} <small>({ta})</small>"
    style = f"color:{color};font-weight:700" if is_yes else ""
    return f'<div class="dp-q" style="{style}">{text}</div>'


def yes_no_row(disease, sid, lang, color):
    """One symptom = one line:  question  ....  [ Yes | No ]"""
    en, ta = SYMPTOM_BY_ID[sid]
    key = qkey(disease, sid)
    st.session_state.setdefault(key, "No")
    left, right = st.columns([3.2, 1.3], vertical_alignment="center")
    left.markdown(question_html(en, ta, lang, color, st.session_state[key] == "Yes"),
                  unsafe_allow_html=True)
    if hasattr(st, "segmented_control"):
        right.segmented_control(en, ["Yes", "No"], key=key, label_visibility="collapsed")
    else:                                            # older Streamlit fallback
        right.radio(en, ["Yes", "No"], key=key, horizontal=True, label_visibility="collapsed")


def clear_answers(disease):
    for sid in disease_symptoms(disease):
        st.session_state[qkey(disease, sid)] = "No"
    st.session_state.pop("result", None)


# ------------------------------------------------------------------ LOGIN PAGE
def login_page():
    st.markdown("<h1 style='text-align:center;margin-bottom:0'>🩺 AI Multiple Disease Prediction</h1>"
                "<p style='text-align:center;color:#607d8b'>Predicting Health, Protecting Lives</p>",
                unsafe_allow_html=True)
    st.markdown(theme.disease_cards(), unsafe_allow_html=True)

    _, mid, _ = st.columns([1, 1.4, 1])
    with mid:
        with st.container(border=True):
            st.markdown("### 🔐 Login")
            with st.form("login_form", border=False):
                name = st.text_input("Name  (பெயர்)", placeholder="Enter your name")
                phone = st.text_input("Phone number  (தொலைபேசி எண்)",
                                      placeholder="10-digit mobile number", max_chars=14)
                go = st.form_submit_button("Login", use_container_width=True, type="primary")
            if go:
                clean_name, clean_phone, err = db.validate_login(name, phone)
                if err:
                    st.error(err)
                else:
                    user, is_new = db.login_user(clean_name, clean_phone)
                    st.session_state.user = user
                    st.session_state.welcome = "Welcome" if is_new else "Welcome back"
                    st.rerun()
            st.caption("New user? Just enter your name and phone number - your account is created automatically.")
        st.caption(DISCLAIMER)


# ------------------------------------------------------------------ HOME PAGE
def home_page(user):
    if st.session_state.get("welcome"):
        st.toast(f"{st.session_state.pop('welcome')}, {user['name']}! 👋")

    st.title(f"Hello, {user['name']} 👋")
    st.write("**Which disease do you want to check?**  Click a card - only that disease's questions will open. "
             "(எந்த நோயை சரிபார்க்க வேண்டுமோ அதை தேர்வு செய்யுங்கள்.)")

    cols = st.columns(5)
    for col, disease in zip(cols, DISEASES):
        with col:
            st.markdown(theme.home_card(disease), unsafe_allow_html=True)
            st.button(f"Check {disease.split()[0]} →", key=f"home_{disease}",
                      on_click=go_to, args=(disease,), use_container_width=True)

    st.markdown("---")
    st.markdown("**How it works:** 1️⃣ Pick a disease  →  2️⃣ Answer Yes / No  →  3️⃣ Get your risk result and advice")
    st.caption(DISCLAIMER)


# ------------------------------------------------------------------ DISEASE PAGE
def disease_page(user, disease, lang):
    theme_d = theme.THEMES[disease]
    color = theme_d["color"]

    st.button("← Back to Home", on_click=go_to, args=("Home",))
    st.markdown(theme.section_header(disease), unsafe_allow_html=True)
    st.write("Answer **Yes** or **No**. If you are not sure, leave it as **No**. "
             "(ஆம் / இல்லை என்று தேர்வு செய்யுங்கள்.)")

    age = st.number_input("Your age  (உங்கள் வயது)", min_value=1, max_value=120, value=30, step=1,
                          key=f"age_{disease_key(disease)}")

    with st.container(border=True):
        for sid in disease_symptoms(disease):
            yes_no_row(disease, sid, lang, color)

    selected = [sid for sid in disease_symptoms(disease)
                if st.session_state.get(qkey(disease, sid)) == "Yes"]
    c1, c2, c3 = st.columns([1.6, 1, 3])
    predict_clicked = c1.button(f"🔍 Predict {disease}", type="primary", use_container_width=True)
    c2.button("Clear all", on_click=clear_answers, args=(disease,), use_container_width=True)
    c3.caption(f"{len(selected)} symptom(s) answered Yes")

    if predict_clicked:
        if not selected:
            st.warning("Please answer **Yes** for at least one symptom you are feeling.")
            st.session_state.pop("result", None)
        else:
            p, level = predictor.predict(disease, age, selected, get_model(disease))
            db.save_prediction(user["phone"], age, selected, f"{disease} - {level} risk", {disease: p})
            st.session_state.result = {"disease": disease, "p": p, "level": level, "selected": selected}

    res = st.session_state.get("result")
    if res and res["disease"] == disease:
        show_result(disease, res)


def show_result(disease, res):
    st.markdown("## Result")
    if disease == "Heart Disease" and emergency_flag(res["selected"]):
        st.error(EMERGENCY_NOTE)

    p, level = res["p"], res["level"]
    st.markdown(theme.risk_card(disease, p * 100, level), unsafe_allow_html=True)
    st.progress(min(max(p, 0.0), 1.0))

    info = ADVICE[disease]
    if level == "High":
        st.error(f"Your answers strongly match **{disease}**. Please meet a doctor soon.")
    elif level == "Moderate":
        st.warning(f"Some of your answers match **{disease}**. It is better to get checked.")
    else:
        st.success(f"Your answers do not strongly match **{disease}**. "
                   "If symptoms continue or get worse, please see a doctor.")

    st.markdown(f"**👨‍⚕️ Doctor to meet:** {info['doctor']}")
    st.markdown(f"**🧪 Tests to ask for:** {info['test']}")
    st.markdown(f"**💡 Tip:** {info['tips']}")
    st.button("← Check another disease", on_click=go_to, args=("Home",), key="another")
    st.caption(DISCLAIMER)


# ------------------------------------------------------------------ HISTORY PAGE
def history_page(user):
    st.title("My History")
    rows = db.get_history(user["phone"])
    if not rows:
        st.info("No checks yet. Pick a disease from Home to try one.")
        return
    for r in rows:
        syms = [SYMPTOM_BY_ID.get(s, (s, s))[0] for s in json.loads(r["symptoms"])]
        with st.expander(f"{r['created_at'].replace('T', '  ')}   —   {r['top_result']}"):
            st.write(f"**Age:** {r['age']}")
            st.write("**Symptoms (Yes):** " + "; ".join(syms))
            probs = json.loads(r["probabilities"])
            top = sorted(probs.items(), key=lambda t: t[1], reverse=True)[:3]
            st.write("**Symptom match:** " + ", ".join(f"{n} {p*100:.0f}%" for n, p in top))


# ------------------------------------------------------------------ ABOUT PAGE
def about_page():
    st.title("About")
    st.markdown(theme.disease_cards(), unsafe_allow_html=True)
    st.write("""
    This system uses **Machine Learning (Random Forest Classification)**. Each of the 5 diseases has its
    **own model and its own page**. You answer simple Yes / No symptom questions and the model tells you
    whether your risk for that disease looks **Low, Moderate or High**.

    You do **not** need any lab report.
    """)
    st.caption(DISCLAIMER)


# ------------------------------------------------------------------ MAIN
user = st.session_state.get("user")
if not user:
    login_page()
    st.stop()

st.session_state.setdefault("page", "Home")
st.sidebar.title("🩺 Disease Prediction")
st.sidebar.markdown(f"👤 **{user['name']}**  \n📱 {user['phone']}")
st.sidebar.radio("Menu", PAGES, key="page")
lang_choice = st.sidebar.selectbox("Language  (மொழி)", ["English + தமிழ்", "English", "தமிழ்"])
lang = "Both" if lang_choice == "English + தமிழ்" else lang_choice
if st.sidebar.button("Logout"):
    for k in list(st.session_state.keys()):
        del st.session_state[k]
    st.rerun()
st.sidebar.markdown("---")
st.sidebar.caption(DISCLAIMER)

page = st.session_state["page"]
if page == "Home":
    home_page(user)
elif page in DISEASES:
    disease_page(user, page, lang)
elif page == "My History":
    history_page(user)
else:
    about_page()
