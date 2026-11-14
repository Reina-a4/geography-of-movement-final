"""Chapter 1 of The Geography of Movement.
Requires Displacement(1).csv in the repository root.
"""
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

MIDNIGHT = "#101820"
AMBER = "#D6AA76"
TEAL = "#79B7B5"
IVORY = "#F5F0E8"

st.html("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
.stApp {background: #101820; color: #F5F0E8; font-family: Inter, Arial, sans-serif;}
.block-container {max-width: 1450px; padding-top: 1.8rem; padding-bottom: 3rem;}
h1,h2,h3 {font-family: Georgia, serif !important; color: #F5F0E8 !important;}
p, label {font-family: Inter, Arial, sans-serif;}
[data-testid="stMetricValue"] {color: #D6AA76; font-family: Inter, Arial, sans-serif;}
[data-testid="stMetricLabel"] {color: #BECACC;}
[data-testid="stVerticalBlockBorderWrapper"] {border-color: #34525A;}
div.stButton button[kind="primary"] {background: #D6AA76; color: #101820; border-color: #D6AA76;}
[data-testid="stSelectSlider"] {accent-color: #79B7B5;}
.topline {color: #D6AA76; letter-spacing: .14em; font-size: .73rem; font-weight: 650;}
.section-label {display:inline-block;background: #D6AA76;color: #101820; padding: .12rem .6rem; border-radius: .32rem; margin-right: .65rem; font-weight: 700; font-family: Inter, Arial, sans-serif; font-size: 1.05rem;}
.subline {color: #C2D0D0; font-size: 1.03rem;}
.note-card {background: #15272E; border: 1px solid #47616A; border-radius: 13px; padding: 22px 24px; color:#E3ECE9; line-height: 1.6;}
.note-heading {color: #D6AA76; font-family: Georgia, serif; font-size: 1.4rem; margin-bottom: .55rem;}
.note-card small {color: #BCCBCC;}
.hr {height:1px; background:#39505A; margin: 16px 0 25px;}
</style>
""")

@st.cache_data(show_spinner=False)
def load_records(path: str):
    records = pd.read_csv(path)
    needed = ["refPeriod", "Latitude", "Longitude", "ID", "Number of People Displaced"]
    missing = [col for col in needed if col not in records.columns]
    if missing:
        raise ValueError("Missing required columns: " + ", ".join(missing))
    records["date"] = pd.to_datetime(records["refPeriod"], errors="coerce")
    for field in ("Latitude", "Longitude", "Number of People Displaced"):
        records[field] = pd.to_numeric(records[field], errors="coerce")
    records = records.dropna(subset=["date", "Latitude", "Longitude"])
    records = records[records["Latitude"].between(33, 35) & records["Longitude"].between(35, 37)]
    return records

root = Path(__file__).resolve().parent.parent
csv_path = root / "Displacement(1).csv"
if not csv_path.exists():
    st.error("Can't find Displacement(1).csv in the project root. Place it alongside app.py, not inside pages/.")
    st.stop()

try:
    df = load_records(str(csv_path))
except Exception as exc:
    st.error(f"Unable to read original AUB dataset: {exc}")
    st.stop()

if df.empty:
    st.error("No dated, mappable displacement observations were found.")
    st.stop()

st.html('<div class="topline">THE GEOGRAPHY OF MOVEMENT · AN INTERACTIVE DATA INVESTIGATION · LEBANON 2023–2024</div>')
nav_home, nav_space = st.columns([1, 5])
with nav_home:
    if st.button("← Home", key="ch1_home_top"):
        st.switch_page(st.session_state["gom_home_page"])
st.html('<div class="hr"></div>')
st.markdown('<span class="section-label">01 /</span> Lebanon Through Time', unsafe_allow_html=True)
st.html('<div class="subline">CHAPTER 01 · FOLLOW THE EVIDENCE — <b>Where Does the Data Take Us?</b> One country. Hundreds of observations. A changing picture.</div>')
st.write("")

available_dates = sorted(df["date"].dt.date.unique())
selected = st.select_slider(
    "Explore reporting dates — show all observations recorded up to this date",
    options=available_dates,
    value=available_dates[len(available_dates)//2],
    format_func=lambda date: date.strftime("%d %b %Y"),
)
# Keep the nationwide 900,000 estimate separate from local report markers.
national = df[(df["ID"] == 163520) & (df["Number of People Displaced"] == 900000)]
local_df = df.drop(index=national.index)
seen = local_df[local_df["date"].dt.date <= selected].copy()
show_nationwide = not national.empty and selected >= national["date"].dt.date.min()
locations = seen.groupby(["Latitude", "Longitude"], as_index=False).agg(
    reports=("ID", "count"),
    largest_reported_estimate=("Number of People Displaced", "max"),
)

left, right = st.columns([1.65, 1], gap="large")
with left:
    fig = px.scatter_map(
        locations,
        lat="Latitude", lon="Longitude", size="reports",
        color_discrete_sequence=[AMBER],
        hover_data={
            "reports": True,
            "largest_reported_estimate": ":,.0f",
            "Latitude": ":.3f", "Longitude": ":.3f",
        },
        size_max=34,
        zoom=7.0,
        center={"lat":33.86,"lon":35.80},
        map_style="open-street-map",
        height=570,
    )
    fig.update_traces(marker={"opacity":0.82})
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor=MIDNIGHT,
        font=dict(family="Inter, Arial, sans-serif", color=IVORY),
        showlegend=False,
    )
    if show_nationwide:
        # The national estimate is shown as a MAP-FRAME banner, never a point pin.
        # Its stored coordinate must not imply the location of displaced people.
        fig.add_shape(
            type="rect", xref="paper", yref="paper",
            x0=0.004, y0=0.005, x1=0.996, y1=0.995,
            line=dict(color=AMBER, width=2), fillcolor="rgba(0,0,0,0)",
            layer="above",
        )
        fig.add_annotation(
            xref="paper", yref="paper", x=0.5, y=0.975,
            text="<b>LEBANON-WIDE ESTIMATE: 900,000 DISPLACED PEOPLE</b>",
            showarrow=False, xanchor="center", yanchor="top",
            font=dict(color=MIDNIGHT, size=13, family="Inter, Arial, sans-serif"),
            bgcolor=AMBER, bordercolor=AMBER, borderwidth=1, borderpad=9,
        )
    st.plotly_chart(fig, use_container_width=True, config={"displaylogo": False})

with right:
    a, b = st.columns(2, gap="small")
    with a:
        st.metric("Reports shown", f"{len(seen):,}")
    with b:
        st.metric("Mapped coordinates", f"{len(locations):,}")
    st.caption(f"Selected reporting date: {selected:%d %b %Y} · Cumulative from {available_dates[0]:%d %b %Y}")
    st.html('''<div class="note-card">
    <div class="note-heading">Your investigation begins here.</div>
    <p>Every point on this map represents a location where the reporter(s) of a given number of displaced individuals recorded their observations. You can follow the changes of a given geographical pattern of reported observations within a given time span.</p>
    <p>Explore the map to find out where there are reports of displacements, which locations are reported most, and many more questions related to this.</p>
    <small>A location where a report was submitted does not have to be the origin or destination of a refugee. This map is based off of the locations in which observations were recorded.</small>
    </div>''')

# Reveal the nationwide observation only when its recorded date is reached.
# Its coordinate is not mapped as a destination or local population count.
if show_nationwide:
    with right:
        st.html('''<div style="border:1px solid #D6AA76;border-radius:13px;background:#192D33;padding:18px 20px;margin-top:15px;">
<div style="color:#D6AA76;font-size:.7rem;font-weight:650;letter-spacing:.12em;">NEW EVIDENCE · 30 SEPTEMBER 2024</div>
<div style="font-family:Georgia,serif;font-size:clamp(36px,4vw,56px);color:#D6AA76;line-height:1.2;margin-top:8px;">900,000</div>
<div style="color:#F5F0E8;font-weight:600;margin-top:5px;">Nationwide displacement estimate</div>
<div style="color:#C2D0D0;font-size:.87rem;line-height:1.55;margin-top:9px;">This estimate covers Lebanon nationally; it does not identify where 900,000 people moved.</div>
<div style="color:#79B7B5;font-family:Georgia,serif;font-size:1.08rem;margin-top:12px;">Where did they go?</div>
</div>''')

st.caption(
    "Source: AUB PKGCubes Displacement dataset (2023–2024), original CSV. "
    "Date is refPeriod. These are observations associated with reported coordinates, "
    "not verified travel trajectories. On 30 Sep 2024, the 900,000 nationwide estimate is shown as a banner across the map and in the side panel, not as a local marker. Map tiles require internet access."
)
st.divider()
if st.button("← Back to investigation home", key="ch1_home_bottom"):
    st.switch_page(st.session_state["gom_home_page"])
st.caption("Next: Chapter 02 · Trace the Journey — explore documented origin–destination connections.")
