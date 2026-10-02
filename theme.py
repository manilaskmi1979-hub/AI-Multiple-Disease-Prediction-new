"""
theme.py
--------
Colours, illustrations (inline SVG icons) and CSS for each disease section.
Each disease has its own colour + picture so users can recognise it quickly.
"""

import base64

# --------------------------------------------------------------------------
# Disease look & feel
# --------------------------------------------------------------------------
THEMES = {
    "Diabetes": {
        "color": "#1E88E5", "light": "#E3F2FD", "dark": "#0D47A1",
        "tagline": "Sugar & urine symptoms  (சர்க்கரை நோய் அறிகுறிகள்)",
    },
    "Heart Disease": {
        "color": "#E53935", "light": "#FFEBEE", "dark": "#B71C1C",
        "tagline": "Chest & heart symptoms  (இதய நோய் அறிகுறிகள்)",
    },
    "Liver Disease": {
        "color": "#EF8A17", "light": "#FFF3E0", "dark": "#B85F00",
        "tagline": "Stomach & skin symptoms  (கல்லீரல் அறிகுறிகள்)",
    },
    "Kidney Disease": {
        "color": "#139A7B", "light": "#E0F5F0", "dark": "#0A6B55",
        "tagline": "Swelling & urine symptoms  (சிறுநீரக அறிகுறிகள்)",
    },
    "Parkinson's Disease": {
        "color": "#7E57C2", "light": "#EDE7F6", "dark": "#4527A0",
        "tagline": "Movement & nerve symptoms  (பார்க்கின்சன் அறிகுறிகள்)",
    },
    "General": {
        "color": "#546E7A", "light": "#ECEFF1", "dark": "#263238",
        "tagline": "General feeling  (பொதுவான உணர்வு)",
    },
    "No Major Concern": {
        "color": "#2E7D32", "light": "#E8F5E9", "dark": "#1B5E20",
        "tagline": "",
    },
}

# --------------------------------------------------------------------------
# Illustrations  (64x64 flat icons, drawn in SVG)
# --------------------------------------------------------------------------
def _svg(body, bg):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">'
            f'<circle cx="32" cy="32" r="31" fill="{bg}"/>{body}</svg>')


ICONS = {
    # blood drop with sugar-cube sparkle
    "Diabetes": _svg(
        '<path d="M32 9 C32 9 15 28 15 40 a17 17 0 0 0 34 0 C49 28 32 9 32 9Z" fill="#1E88E5"/>'
        '<path d="M23 40 a9 9 0 0 0 7 9" stroke="#fff" stroke-width="3.5" fill="none" stroke-linecap="round" opacity=".85"/>'
        '<rect x="39" y="34" width="8" height="8" rx="1.5" fill="#fff" transform="rotate(15 43 38)"/>'
        '<path d="M50 14 v8 M46 18 h8" stroke="#1E88E5" stroke-width="3" stroke-linecap="round"/>',
        "#E3F2FD"),
    # heart with ECG line
    "Heart Disease": _svg(
        '<path d="M32 54 C11 40 8 29 8 22 a12.5 12.5 0 0 1 24-5 a12.5 12.5 0 0 1 24 5 c0 7-3 18-24 32z" fill="#E53935"/>'
        '<path d="M13 31 h10 l4-8 l6 16 l4-8 h14" stroke="#fff" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round"/>',
        "#FFEBEE"),
    # liver lobe + gallbladder
    "Liver Disease": _svg(
        '<path d="M7 27 C7 18 17 13 32 14 C48 15 58 22 57 31 C56 41 46 46 38 45 C31 44 28 40 20 40 C11 40 7 34 7 27Z" fill="#EF8A17"/>'
        '<path d="M30 15 C28 24 30 34 36 44" stroke="#B85F00" stroke-width="2.6" fill="none" stroke-linecap="round"/>'
        '<ellipse cx="42" cy="48" rx="5" ry="7" fill="#2E9E4F" transform="rotate(-20 42 48)"/>'
        '<circle cx="19" cy="27" r="2.2" fill="#fff" opacity=".7"/>',
        "#FFF3E0"),
    # kidney bean
    "Kidney Disease": _svg(
        '<path d="M42 10 C54 12 58 25 52 38 C47 50 36 56 27 53 C19 50 19 42 26 38 C32 35 32 31 26 28 C17 24 14 15 22 10 C28 7 35 9 42 10Z" fill="#139A7B"/>'
        '<path d="M26 28 C20 26 20 20 25 17" stroke="#fff" stroke-width="2.6" fill="none" stroke-linecap="round" opacity=".8"/>'
        '<path d="M44 20 C47 26 46 33 42 39" stroke="#0A6B55" stroke-width="2.6" fill="none" stroke-linecap="round"/>',
        "#E0F5F0"),
    # brain
    "Parkinson's Disease": _svg(
        '<path d="M32 12 C28 8 18 9 16 17 C9 18 8 28 13 32 C9 38 14 47 21 46 C23 52 32 54 32 54 Z" fill="#7E57C2"/>'
        '<path d="M32 12 C36 8 46 9 48 17 C55 18 56 28 51 32 C55 38 50 47 43 46 C41 52 32 54 32 54 Z" fill="#9575CD"/>'
        '<path d="M32 13 V53" stroke="#fff" stroke-width="2.4" opacity=".8"/>'
        '<path d="M18 26 c5-1 7 3 12 2 M20 37 c4 1 6-2 10-1 M46 26 c-5-1-7 3-12 2 M44 37 c-4 1-6-2-10-1" stroke="#fff" stroke-width="2.2" fill="none" stroke-linecap="round" opacity=".85"/>',
        "#EDE7F6"),
    # tired face for "general"
    "General": _svg(
        '<circle cx="32" cy="32" r="19" fill="#546E7A"/>'
        '<path d="M22 28 h7 M35 28 h7" stroke="#fff" stroke-width="3" stroke-linecap="round"/>'
        '<path d="M24 41 q8-5 16 0" stroke="#fff" stroke-width="3" fill="none" stroke-linecap="round"/>',
        "#ECEFF1"),
    # tick for healthy
    "No Major Concern": _svg(
        '<circle cx="32" cy="32" r="19" fill="#2E7D32"/>'
        '<path d="M22 33 l7 7 l14-15" stroke="#fff" stroke-width="4.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>',
        "#E8F5E9"),
}


def icon_img(name, size=48):
    """<img> tag with the icon embedded (works inside st.markdown)."""
    b64 = base64.b64encode(ICONS[name].encode()).decode()
    return (f'<img src="data:image/svg+xml;base64,{b64}" width="{size}" height="{size}" '
            f'style="vertical-align:middle;border-radius:50%"/>')


def section_header(name, subtitle=None):
    t = THEMES[name]
    sub = subtitle or t["tagline"]
    title = name if name != "General" else "General"
    return (
        f'<div class="dp-head" style="background:linear-gradient(90deg,{t["light"]},#ffffff);'
        f'border-left:8px solid {t["color"]}">'
        f'{icon_img(name, 52)}'
        f'<div><div class="dp-title" style="color:{t["dark"]}">{title}</div>'
        f'<div class="dp-sub">{sub}</div></div></div>'
    )


def disease_cards(names=None):
    """Row of the 5 disease cards (used on login page and top of the checker)."""
    names = names or ["Diabetes", "Heart Disease", "Liver Disease", "Kidney Disease", "Parkinson's Disease"]
    cards = ""
    for n in names:
        t = THEMES[n]
        cards += (f'<div class="dp-card" style="background:{t["light"]};border-bottom:5px solid {t["color"]}">'
                  f'{icon_img(n, 56)}<div style="color:{t["dark"]};font-weight:700;margin-top:6px">{n}</div></div>')
    return f'<div class="dp-cards">{cards}</div>'


def result_card(name, percent, headline):
    t = THEMES[name]
    return (
        f'<div class="dp-result" style="background:linear-gradient(135deg,{t["light"]},#fff);'
        f'border:2px solid {t["color"]}">{icon_img(name, 84)}'
        f'<div><div style="font-size:.9rem;color:{t["dark"]};font-weight:600">{headline}</div>'
        f'<div style="font-size:1.9rem;font-weight:800;color:{t["color"]}">{name}</div>'
        f'<div style="font-size:1.1rem;color:{t["dark"]}">{percent:.0f}% match</div></div></div>'
    )


RISK_COLORS = {"High": "#D32F2F", "Moderate": "#F9A825", "Low": "#2E7D32"}
RISK_TEXT = {"High": "High risk  (அதிக ஆபத்து)", "Moderate": "Moderate risk  (நடுத்தர ஆபத்து)",
             "Low": "Low risk  (குறைந்த ஆபத்து)"}


def risk_card(disease, percent, level):
    """Big result card: disease icon + risk level badge + % match."""
    t = THEMES[disease]
    rc = RISK_COLORS[level]
    return (
        f'<div class="dp-result" style="background:linear-gradient(135deg,{t["light"]},#fff);'
        f'border:2px solid {t["color"]}">{icon_img(disease, 84)}'
        f'<div><div style="font-size:.95rem;color:{t["dark"]};font-weight:600">Result for {disease}</div>'
        f'<div style="display:inline-block;margin:4px 0;padding:4px 14px;border-radius:20px;'
        f'background:{rc};color:#fff;font-size:1.3rem;font-weight:800">{RISK_TEXT[level]}</div>'
        f'<div style="font-size:1.05rem;color:{t["dark"]}">Symptom match: <b>{percent:.0f}%</b></div></div></div>'
    )


def home_card(disease):
    """Static card for the Home page (a button is placed below it by app.py)."""
    t = THEMES[disease]
    return (f'<div class="dp-card" style="background:{t["light"]};border-bottom:5px solid {t["color"]};'
            f'padding:18px 8px">{icon_img(disease, 72)}'
            f'<div style="color:{t["dark"]};font-weight:800;font-size:1.05rem;margin-top:8px">{disease}</div>'
            f'<div style="color:#607d8b;font-size:.78rem;margin-top:2px">{t["tagline"]}</div></div>')


CSS = """
<style>
.dp-head{display:flex;align-items:center;gap:14px;padding:10px 14px;border-radius:12px;margin:6px 0 10px 0}
.dp-title{font-size:1.35rem;font-weight:800;line-height:1.2}
.dp-sub{font-size:.85rem;color:#607d8b}
.dp-cards{display:flex;flex-wrap:wrap;gap:12px;margin:8px 0 16px 0}
.dp-card{flex:1 1 130px;text-align:center;padding:14px 8px;border-radius:14px;font-size:.9rem}
.dp-result{display:flex;align-items:center;gap:18px;padding:16px 20px;border-radius:16px;margin:8px 0 14px 0}
.dp-q{font-size:1rem;padding-top:4px}
.dp-q small{color:#78909c}
</style>
"""
