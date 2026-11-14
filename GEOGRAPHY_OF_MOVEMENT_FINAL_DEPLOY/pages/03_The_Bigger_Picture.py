"""Chapter 03 — The Illusion of Precision. Self-contained Streamlit page.

Uses the original AUB PKGCubes Displacement(1).csv. Reporting windows
are derived from the original record descriptions. The example illustrates a
RISK of duplicated coverage, not proof of duplicated people.
"""
from pathlib import Path
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent.parent
CSV = ROOT / "Displacement(1).csv"

st.html("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
.stApp,[data-testid="stAppViewContainer"]{background:#101820!important;color:#F5F0E8!important}
.block-container{max-width:1130px;padding-top:1.4rem;padding-bottom:3.5rem}
[data-testid="stSidebar"],[data-testid="collapsedControl"]{display:none!important}
.ch3-eyebrow{color:#D6AA76;letter-spacing:.16em;font:700 12px Inter,Arial,sans-serif;margin:18px 0 10px}
.ch3-title{font:normal clamp(36px,5vw,57px)/1.1 Georgia,serif;color:#F5F0E8;margin:8px 0 13px}
.ch3-lead{font:italic 22px/1.4 Georgia,serif;color:#79B7B5;margin:0 0 15px}
.ch3-body{font:15px/1.73 Inter,Arial,sans-serif;color:#D3E0E1;max-width:880px;margin:0 0 16px}
.ch3-card{background:#1A2931;border:1px solid #3A535A;border-radius:16px;padding:22px 25px;margin:14px 0}
.ch3-step{color:#D6AA76;letter-spacing:.12em;font:700 11px Inter,Arial,sans-serif;margin:22px 0 10px}
.ch3-heading{font:normal 25px/1.28 Georgia,serif;color:#F5F0E8;margin-bottom:10px}
.ch3-hint{font:13px/1.65 Inter,Arial,sans-serif;color:#B2C4C7}
.ch3-strong{color:#F5F0E8;font:600 15px/1.65 Inter,Arial,sans-serif}
.ch3-result{background:#20343B;border:1px solid #D6AA76;border-radius:14px;padding:21px 22px;margin:13px 0}
.ch3-result-title{color:#D6AA76;font:600 16px/1.5 Inter,Arial,sans-serif;margin-bottom:8px}
.ch3-result-body{color:#E5EEED;font:14px/1.8 Inter,Arial,sans-serif}
.ch3-number{color:#D6AA76;font:normal 32px/1.2 Georgia,serif;margin:6px 0}
.ch3-takeaway{border-left:3px solid #D6AA76;background:#22353B;border-radius:6px;padding:17px 21px;color:#F5F0E8;font:italic 23px/1.48 Georgia,serif;margin:16px 0}
.stButton button{background:#21353D!important;color:#F5F0E8!important;border:1px solid #55737A!important;border-radius:10px!important;min-height:47px!important}
.stButton button:hover{border-color:#D6AA76!important;color:#D6AA76!important}
.stSlider [data-baseweb="slider"] [role="slider"]{background:#D6AA76!important}
[data-testid="stMarkdownContainer"] p{color:#E1E8E8}
@media(max-width:700px){.ch3-card{padding:15px}.ch3-title{font-size:35px}}
</style>
""")

# Uses the explicit navigation system already set up by the user's homepage.
if st.button("← Home", key="ch3_home"):
    home = st.session_state.get("gom_home_page")
    if home is not None:
        st.switch_page(home)
    else:
        st.error("Open the website from the homepage to use navigation.")

st.html("""
<div class="ch3-eyebrow">CHAPTER 03 · THE ILLUSION OF PRECISION</div>
<div class="ch3-title">Can You Spot the Counting Trap?</div>
<p class="ch3-lead">Two reports. Two numbers. One important question.</p>
<p class="ch3-body">Imagine one report counts people in individual places across Lebanon. Another estimates the number for the whole country. Both cover some of the same days.</p>
<p class="ch3-body">If you add those numbers, <b>could you be counting some people twice?</b></p>
""")

if not CSV.is_file():
    st.error("The original Displacement(1).csv is missing from the main geography-of-movement folder.")
    st.stop()

@st.cache_data(show_spinner=False)
def load_data(path):
    df = pd.read_csv(path)
    cols = {"ID", "Description", "Number of People Displaced", "refPeriod"}
    missing = cols - set(df.columns)
    if missing:
        raise ValueError("Missing CSV columns: " + ", ".join(sorted(missing)))
    df["ID"] = pd.to_numeric(df["ID"], errors="coerce")
    df["Number of People Displaced"] = pd.to_numeric(df["Number of People Displaced"], errors="coerce")
    return df

try:
    df = load_data(str(CSV))
    local = df[
        df["Description"].fillna("").str.contains(r"19 September\s*-\s*25 September",case=False,regex=True)
        & (df["refPeriod"].astype(str) == "9/25/2024")
    ]
    nation = df[(df["ID"] == 163520) & (df["refPeriod"].astype(str) == "9/30/2024")]
    if len(local) != 25 or len(nation) != 1:
        raise ValueError("Source records do not match the expected reporting windows")
    local_sum = int(local["Number of People Displaced"].sum())
    nation_sum = int(nation["Number of People Displaced"].iloc[0])
except Exception as exc:
    st.error("Could not verify the September 2024 records against the original CSV: " + str(exc))
    st.stop()

st.html('<div class="ch3-step">01 / YOU DECIDE</div><div class="ch3-heading">What would you do?</div>')
left, right = st.columns(2, gap="medium")
with left:
    choose_add = st.button("Add the two numbers", key="ch3_add", use_container_width=True)
with right:
    choose_check = st.button("Check what they count first", key="ch3_check", use_container_width=True)
if choose_add:
    st.session_state["ch3_answer"] = "add"
elif choose_check:
    st.session_state["ch3_answer"] = "check"
choice = st.session_state.get("ch3_answer")

if choice:
    if choice == "add":
        headline = "Here's the catch: the sum may count people twice."
    else:
        headline = "Exactly. First, check whether the reports cover the same people."
    st.html(f"""
    <div class="ch3-result"><div class="ch3-result-title">{headline}</div>
    <div class="ch3-result-body">A person included in a local report might already be included in the nationwide estimate.
    Adding both figures could count that person twice.<br><br>
    <b>We do not know whether that happened.</b> We only know the reporting dates overlap, so the figures cannot automatically be treated as separate people.</div></div>
    """)
else:
    st.html('<div class="ch3-hint">Choose an answer to uncover the catch. There is no penalty for guessing.</div>')

st.html("""
<div class="ch3-step">02 / LOOK AT THE ACTUAL REPORTS</div>
<div class="ch3-heading">Now, see why we asked.</div>
<p class="ch3-body">In the AUB dataset, 25 observations describe individual districts or localities over <b>19–25 September 2024</b>. A separate nationwide estimate describes <b>23–30 September 2024</b>. Their time periods cross.</p>
<div class="ch3-hint">Select which reporting windows you want to inspect, then move the date slider.</div>
""")
col_a, col_b = st.columns(2)
with col_a:
    show_local = st.checkbox("Individual locations", value=True, key="ch3_local")
with col_b:
    show_nation = st.checkbox("Whole-country estimate", value=True, key="ch3_nation")

# Data-linked reporting-window diagram. Bars show coverage periods, not daily movement.
WIDTH, HEIGHT = 970, 184
x0, x1 = 173, 940
point = lambda date: x0 + (date - 19) * (x1 - x0) / 11
svg = [f'<svg viewBox="0 0 {WIDTH} {HEIGHT}" style="display:block;width:100%;height:auto" role="img" aria-label="Individual-location reporting 19 to 25 September and nationwide reporting 23 to 30 September 2024">']
if show_local and show_nation:
    x = point(23)-13; w = point(25)-point(23)+26
    svg.append(f'<rect x="{x:.1f}" y="5" width="{w:.1f}" height="117" rx="6" fill="#D6AA76" fill-opacity=".13" stroke="#D6AA76" stroke-opacity=".45" stroke-dasharray="4 4"/>')
    svg.append(f'<text x="{(point(23)+point(25))/2:.1f}" y="16" fill="#D6AA76" font-size="12" text-anchor="middle" font-family="Arial">OVERLAP</text>')
svg.extend([
    '<text x="8" y="55" fill="#F5F0E8" font-size="15" font-family="Arial">Individual places</text>',
    '<text x="8" y="103" fill="#F5F0E8" font-size="15" font-family="Arial">Whole country</text>',
    f'<rect x="{point(19)-12:.1f}" y="33" width="{point(25)-point(19)+24:.1f}" height="26" rx="6" fill="{("#79B7B5" if show_local else "#536369")}" opacity="{1 if show_local else .18}"/>',
    f'<rect x="{point(23)-12:.1f}" y="81" width="{point(30)-point(23)+24:.1f}" height="26" rx="6" fill="{("#D6AA76" if show_nation else "#536369")}" opacity="{1 if show_nation else .18}"/>',
])
for d in range(19,31):
    svg.append(f'<text x="{point(d):.1f}" y="144" fill="#ACBFC1" text-anchor="middle" font-size="12" font-family="Arial">{d}</text>')
svg.append('<text x="560" y="169" fill="#ACBFC1" text-anchor="middle" font-size="12" font-family="Arial">SEPTEMBER 2024 · REPORTING WINDOWS</text></svg>')
st.html('<div class="ch3-card">' + ''.join(svg) + '</div>')

selected = st.slider("Choose a September date", 19, 30, 23, key="ch3_day")
a = show_local and 19 <= selected <= 25
b = show_nation and 23 <= selected <= 30
if a and b:
    msg = f"<b>{selected} September:</b> Both reporting periods include this day. That means we must check their coverage before adding the figures. It does not prove the same person was counted twice."
elif a:
    msg = f"<b>{selected} September:</b> This date falls inside the individual-location reporting period."
elif b:
    msg = f"<b>{selected} September:</b> This date falls inside the whole-country reporting period."
else:
    msg = "No currently selected reporting window includes this date. Try turning on both layers."
st.html(f'<div class="ch3-result"><div class="ch3-result-body">{msg}</div></div>')

st.html('<div class="ch3-step">03 / THE NUMBERS BEHIND THE QUESTION</div>')
a_col, b_col = st.columns(2)
with a_col:
    st.html(f'<div class="ch3-card"><div class="ch3-hint">25 observations · individual locations</div><div class="ch3-number">{local_sum:,}</div><div class="ch3-hint">Sum of their reported figures. Not a verified count of distinct people.</div></div>')
with b_col:
    st.html(f'<div class="ch3-card"><div class="ch3-hint">One whole-country estimate</div><div class="ch3-number">{nation_sum:,}</div><div class="ch3-hint">Nationwide estimate, reported on 30 September 2024.</div></div>')

if st.button("Show what happens if we simply add them", key="ch3_math"):
    st.session_state["ch3_show_math"] = True
if st.session_state.get("ch3_show_math"):
    st.html(f'''<div class="ch3-result"><div class="ch3-result-title">{local_sum:,} + {nation_sum:,} = {local_sum + nation_sum:,}</div>
    <div class="ch3-result-body">The arithmetic is correct. But <b>{local_sum + nation_sum:,} is not a verified total of different people.</b> The records have different geographic coverage and overlapping time windows, and we cannot establish which individuals appear in both.</div></div>''')

st.html('''
<div class="ch3-step">04 / THE TAKEAWAY</div>
<div class="ch3-takeaway">More numbers do not always mean more people. Before adding reports together, we need to know what each one counts.</div>
<p class="ch3-body">Chapter 1 explored where observations were recorded. Chapter 2 traced documented connections between places. Chapter 3 asks us to read the numbers responsibly: <b>who was counted, where, and during which period?</b></p>
<p class="ch3-hint">Source: AUB PKGCubes Displacement dataset. The 25 location observations describe 19–25 September 2024 and were recorded with a 25 September reference date. The nationwide observation (ID 163520) describes 23–30 September 2024 and was recorded with a 30 September reference date. The highlighted overlap indicates shared calendar dates, not confirmed duplicate individuals; neither bar is a daily movement count.</p>
''')
