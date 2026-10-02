"""
symptoms.py
-----------
Single source of truth for:
  * the symptom questions shown to the user (English + Tamil, plain language)
  * how likely each symptom is in each disease (used to generate training data)
  * advice / specialist for each disease

Nothing here needs medical lab values - every question is something a normal
person can answer with Yes / No.
"""

# --------------------------------------------------------------------------
# Categories (order = order shown on the page)
# --------------------------------------------------------------------------
CATEGORIES = {
    "general":  "General feeling  (பொதுவான உணர்வு)",
    "urine":    "Urine & thirst  (சிறுநீர் & தாகம்)",
    "chest":    "Chest & heart  (நெஞ்சு & இதயம்)",
    "stomach":  "Stomach & skin  (வயிறு & தோல்)",
    "swelling": "Swelling & pain  (வீக்கம் & வலி)",
    "nerves":   "Movement & nerves  (இயக்கம் & நரம்பு)",
    "history":  "Habits & family history  (பழக்கவழக்கம் & குடும்ப வரலாறு)",
}

# --------------------------------------------------------------------------
# (id, English question, Tamil question, category)
# --------------------------------------------------------------------------
SYMPTOMS = [
    # General
    ("fatigue",         "Feeling very tired or weak all the time",       "எப்போதும் மிகவும் சோர்வாக / பலவீனமாக இருப்பது", "general"),
    ("weight_loss",     "Losing weight without trying",                  "முயற்சி செய்யாமல் எடை குறைவது",                 "general"),
    ("loss_appetite",   "Not feeling hungry / loss of appetite",         "பசி இல்லாமை",                                   "general"),
    ("increased_hunger","Feeling extremely hungry very often",           "அடிக்கடி அதிக பசி எடுப்பது",                    "general"),
    ("dizziness",       "Dizziness or fainting",                         "தலைச்சுற்றல் / மயக்கம்",                         "general"),
    ("blurred_vision",  "Blurred vision",                                "பார்வை மங்கலாக தெரிவது",                         "general"),
    ("frequent_infections", "Getting infections again and again",        "அடிக்கடி தொற்று / நோய் வருவது",                  "general"),
    ("sleep_problems",  "Disturbed sleep / moving or shouting in sleep", "தூக்கத்தில் தொந்தரவு / தூக்கத்தில் கை கால் அசைப்பது", "general"),

    # Urine & thirst
    ("frequent_urination", "Passing urine very often during the day",    "பகலில் அடிக்கடி சிறுநீர் போவது",                "urine"),
    ("night_urination", "Waking up at night to pass urine",              "இரவில் சிறுநீருக்காக எழுந்திருப்பது",           "urine"),
    ("excessive_thirst","Feeling very thirsty all the time",             "எப்போதும் அதிக தாகம் எடுப்பது",                  "urine"),
    ("reduced_urine",   "Passing much less urine than usual",            "வழக்கத்தை விட சிறுநீர் மிகவும் குறைவு",          "urine"),
    ("foamy_urine",     "Foamy / bubbly urine",                          "நுரையுடன் சிறுநீர் வருவது",                      "urine"),
    ("blood_urine",     "Blood in urine (red / pink urine)",             "சிறுநீரில் இரத்தம் (சிவப்பு / இளஞ்சிவப்பு)",     "urine"),
    ("dark_urine",      "Dark yellow or brown urine",                    "அடர் மஞ்சள் / பழுப்பு நிற சிறுநீர்",             "urine"),

    # Chest & heart
    ("chest_pain",      "Chest pain, pressure or tightness",             "நெஞ்சு வலி / அழுத்தம் / இறுக்கம்",              "chest"),
    ("breathless",      "Breathlessness (even on light work)",           "மூச்சுத் திணறல் (லேசான வேலைக்கும்)",            "chest"),
    ("arm_jaw_pain",    "Pain spreading to left arm, jaw or back",       "இடது கை / தாடை / முதுகுக்கு வலி பரவுவது",        "chest"),
    ("palpitations",    "Heart racing or pounding",                      "இதயம் படபடப்பு / வேகமாக துடிப்பது",              "chest"),
    ("cold_sweat",      "Sudden cold sweat",                             "திடீர் குளிர் வியர்வை",                          "chest"),

    # Stomach & skin
    ("jaundice",        "Yellow colour of skin or eyes",                 "தோல் / கண் மஞ்சள் நிறமாக மாறுவது",              "stomach"),
    ("pale_stool",      "Pale / clay coloured stools",                   "வெளிரிய நிற மலம்",                               "stomach"),
    ("abdominal_pain",  "Pain in upper right side of belly",             "வயிற்றின் வலது மேல் பக்கம் வலி",                 "stomach"),
    ("abdominal_swelling", "Swollen belly",                              "வயிறு வீங்கியிருப்பது",                           "stomach"),
    ("nausea",          "Nausea or vomiting",                            "குமட்டல் / வாந்தி",                               "stomach"),
    ("itching",         "Itchy skin all over the body",                  "உடல் முழுவதும் அரிப்பு",                         "stomach"),
    ("easy_bruising",   "Bruises or bleeds easily",                      "எளிதில் தோலில் காயம் / இரத்தக்கசிவு",            "stomach"),
    ("slow_healing",    "Cuts and wounds heal very slowly",              "காயங்கள் ஆற மிகவும் தாமதமாவது",                  "stomach"),
    ("dark_skin",       "Dark patches on neck or armpits",               "கழுத்து / அக்குளில் கருமையான திட்டுகள்",         "stomach"),

    # Swelling & pain
    ("swelling",        "Swelling in feet or ankles",                    "கால் / கணுக்கால் வீக்கம்",                       "swelling"),
    ("face_swelling",   "Puffy face or swelling around eyes",            "முகம் / கண்ணைச் சுற்றி வீக்கம்",                 "swelling"),
    ("back_pain",       "Pain in lower back or sides",                   "இடுப்பு / பக்கவாட்டில் வலி",                     "swelling"),
    ("muscle_cramps",   "Frequent muscle cramps",                        "அடிக்கடி தசைப்பிடிப்பு",                          "swelling"),
    ("numbness",        "Tingling or numbness in hands / feet",          "கை / கால் மரத்துப் போதல் / கூச்சம்",             "swelling"),

    # Movement & nerves
    ("tremor",          "Hand shaking when resting",                     "ஓய்வில் இருக்கும்போது கை நடுக்கம்",              "nerves"),
    ("slow_movement",   "Moving / walking slower than before",           "முன்பை விட மெதுவாக நடப்பது / அசைவது",            "nerves"),
    ("stiffness",       "Stiff arms, legs or neck",                      "கை, கால், கழுத்து இறுக்கம்",                     "nerves"),
    ("balance",         "Difficulty keeping balance / falling",          "சமநிலை தவறுவது / விழுவது",                       "nerves"),
    ("small_handwriting","Handwriting has become very small",            "கையெழுத்து மிகச் சிறியதாக மாறியது",              "nerves"),
    ("soft_voice",      "Voice has become soft or low",                  "குரல் மெல்லியதாக / தாழ்வாக மாறியது",             "nerves"),
    ("masked_face",     "Face shows little expression",                  "முகத்தில் உணர்ச்சி வெளிப்பாடு குறைவு",           "nerves"),
    ("shuffling",       "Walking with small shuffling steps",            "சிறு சிறு அடிகளாக இழுத்து நடப்பது",              "nerves"),
    ("loss_smell",      "Reduced sense of smell",                        "வாசனை உணர்வு குறைவு",                            "nerves"),
    ("constipation",    "Long-standing constipation",                    "நீண்ட நாள் மலச்சிக்கல்",                         "nerves"),

    # History
    ("high_bp",         "Told you have high blood pressure",             "உயர் இரத்த அழுத்தம் உள்ளதாக சொல்லப்பட்டது",      "history"),
    ("overweight",      "Overweight / big belly",                        "அதிக எடை / தொப்பை",                              "history"),
    ("smoking",         "Smoke or chew tobacco",                         "புகைப்பிடித்தல் / புகையிலை",                     "history"),
    ("alcohol",         "Drink alcohol regularly",                       "தொடர்ந்து மது அருந்துதல்",                       "history"),
    ("family_diabetes", "Parents / siblings have diabetes",              "பெற்றோர் / உடன்பிறந்தோருக்கு சர்க்கரை நோய்",     "history"),
    ("family_heart",    "Family history of heart attack",                "குடும்பத்தில் மாரடைப்பு வரலாறு",                  "history"),
]

SYMPTOM_IDS = [s[0] for s in SYMPTOMS]
FEATURES = ["age"] + SYMPTOM_IDS     # exact column order used by the model

# --------------------------------------------------------------------------
# Diseases (class labels). "None" = no major concern from these symptoms.
# --------------------------------------------------------------------------
NONE_LABEL = "No Major Concern"
DISEASES = ["Diabetes", "Heart Disease", "Liver Disease", "Kidney Disease", "Parkinson's Disease"]
CLASSES = DISEASES + [NONE_LABEL]

# Probability that a person WITH the disease reports each symptom
PROFILES = {
    "Diabetes": {
        "frequent_urination": .85, "excessive_thirst": .85, "increased_hunger": .60,
        "weight_loss": .45, "blurred_vision": .50, "slow_healing": .50, "numbness": .45,
        "fatigue": .70, "frequent_infections": .35, "dark_skin": .35, "night_urination": .40,
        "family_diabetes": .50, "overweight": .50, "itching": .15,
    },
    "Heart Disease": {
        "chest_pain": .85, "breathless": .75, "arm_jaw_pain": .55, "palpitations": .55,
        "dizziness": .50, "cold_sweat": .45, "swelling": .40, "fatigue": .60,
        "high_bp": .55, "family_heart": .45, "nausea": .25, "smoking": .35, "overweight": .35,
    },
    "Liver Disease": {
        "jaundice": .75, "dark_urine": .65, "pale_stool": .40, "abdominal_pain": .60,
        "abdominal_swelling": .50, "nausea": .60, "loss_appetite": .65, "itching": .40,
        "fatigue": .65, "easy_bruising": .35, "alcohol": .50, "weight_loss": .30, "swelling": .20,
    },
    "Kidney Disease": {
        "face_swelling": .60, "swelling": .65, "reduced_urine": .50, "foamy_urine": .55,
        "blood_urine": .30, "night_urination": .55, "itching": .45, "muscle_cramps": .45,
        "nausea": .50, "fatigue": .70, "back_pain": .45, "high_bp": .60, "loss_appetite": .50,
        "breathless": .30,
    },
    "Parkinson's Disease": {
        "tremor": .85, "slow_movement": .80, "stiffness": .75, "balance": .60,
        "small_handwriting": .55, "soft_voice": .50, "masked_face": .45, "shuffling": .50,
        "loss_smell": .40, "sleep_problems": .45, "constipation": .45, "dizziness": .20,
        "fatigue": .30,
    },
}

# Background chance of a symptom in a person who does NOT have that disease
DEFAULT_BASE = 0.03
BASELINE = {
    "fatigue": .20, "nausea": .08, "dizziness": .08, "breathless": .06, "loss_appetite": .06,
    "back_pain": .10, "constipation": .10, "sleep_problems": .10, "high_bp": .15,
    "alcohol": .15, "smoking": .12, "overweight": .25, "itching": .05, "numbness": .05,
    "swelling": .04, "muscle_cramps": .06, "blurred_vision": .05, "weight_loss": .04,
}

# Typical age range (low, high) per class, used for the "age" feature
AGE_RANGE = {
    "Diabetes": (25, 80), "Heart Disease": (35, 85), "Liver Disease": (20, 75),
    "Kidney Disease": (20, 80), "Parkinson's Disease": (50, 85), NONE_LABEL: (15, 80),
}

# --------------------------------------------------------------------------
# What to tell the user
# --------------------------------------------------------------------------
ADVICE = {
    "Diabetes": {
        "doctor": "General Physician / Diabetologist",
        "test": "Fasting blood sugar, post-meal sugar and HbA1c",
        "tips": "Cut down sugar and sweets, walk 30 minutes daily, and avoid skipping meals.",
    },
    "Heart Disease": {
        "doctor": "Cardiologist",
        "test": "ECG, BP check, lipid profile (cholesterol) and Echo / TMT if advised",
        "tips": "Avoid oily food, salt and smoking. Do not ignore chest pain.",
    },
    "Liver Disease": {
        "doctor": "Gastroenterologist / Hepatologist",
        "test": "Liver function test (LFT) and abdominal ultrasound",
        "tips": "Avoid alcohol and self-medication (especially painkillers) until you see a doctor.",
    },
    "Kidney Disease": {
        "doctor": "Nephrologist",
        "test": "Blood urea, serum creatinine, urine routine and BP check",
        "tips": "Drink water as advised, cut down salt, and avoid painkillers like diclofenac without a doctor's advice.",
    },
    "Parkinson's Disease": {
        "doctor": "Neurologist",
        "test": "Neurological examination (the doctor decides further tests)",
        "tips": "Stay active with walking and gentle exercise, and make your home fall-safe.",
    },
    NONE_LABEL: {
        "doctor": "General Physician (if symptoms continue)",
        "test": "Routine health check-up once a year",
        "tips": "Your symptoms do not strongly match any of the 5 diseases. Eat well, exercise, sleep well.",
    },
}

EMERGENCY_NOTE = (
    "🚨 **Chest pain with pain spreading to the arm/jaw, sweating or breathlessness can be a heart attack. "
    "Do not wait - call 108 (ambulance) or go to the nearest hospital immediately.**"
)


def emergency_flag(selected):
    """True if the combination of selected symptoms looks like a possible heart emergency."""
    s = set(selected)
    return "chest_pain" in s and bool(s & {"arm_jaw_pain", "cold_sweat", "breathless"})


def disease_symptoms(disease):
    """Symptoms asked on one disease's page (most telling first)."""
    return sorted(PROFILES[disease], key=lambda s: -PROFILES[disease][s])


def disease_features(disease):
    """Exact feature order for that disease's model: age + its symptoms."""
    return ["age"] + disease_symptoms(disease)


def disease_key(disease):
    """File-safe key, e.g. "Parkinson's Disease" -> "parkinsons"."""
    return {"Diabetes": "diabetes", "Heart Disease": "heart", "Liver Disease": "liver",
            "Kidney Disease": "kidney", "Parkinson's Disease": "parkinsons"}[disease]
