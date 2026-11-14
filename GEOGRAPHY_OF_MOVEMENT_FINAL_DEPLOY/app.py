"""The Geography of Movement — homepage with consistent chapter cards."""
import streamlit as st

st.set_page_config(
    page_title="The Geography of Movement",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def homepage():
    st.html("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    .stApp,[data-testid="stAppViewContainer"] {background:#101820;color:#F5F0E8;}
    .block-container {max-width:1160px;padding-top:5rem;padding-bottom:3rem;}
    .gom-hero {text-align:center;padding:0 1rem 3.5rem;}
    .gom-eyebrow {color:#D6AA76;letter-spacing:.17em;font:700 12px Inter,Arial,sans-serif;}
    .gom-title {font:normal clamp(38px,5vw,68px)/1.13 Georgia,serif;color:#F5F0E8;margin:26px 0 20px;}
    .gom-subtitle {font:500 clamp(16px,2vw,20px) Inter,Arial,sans-serif;color:#79B7B5;}
    .gom-rule {width:60px;height:3px;background:#D6AA76;border-radius:3px;margin:28px auto;}
    .gom-description {font:15px/1.7 Inter,Arial,sans-serif;color:#C2CDCF;}
    .gom-grid {display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:22px;align-items:stretch;}
    .gom-card {
        box-sizing:border-box;min-width:0;min-height:280px;
        padding:32px 22px;display:flex;flex-direction:column;
        align-items:center;justify-content:flex-start;text-align:center;
        border:1px solid #34464B;border-radius:18px;
        background:#18262D;text-decoration:none !important;
    }
    .gom-card * {box-sizing:border-box;}
    .gom-num {color:#D6AA76 !important;font:normal 54px/1.1 Georgia,serif !important;margin:0 0 18px;}
    .gom-card-title {color:#F5F0E8 !important;font:600 20px/1.3 Inter,Arial,sans-serif !important;margin:0 0 18px;min-height:52px;}
    .gom-card-desc {color:#BFCBCD !important;font:400 15px/1.6 Inter,Arial,sans-serif !important;margin:0;}
    .gom-coming {display:block;margin-top:12px;font:500 13px/1.5 Inter,Arial,sans-serif;color:#9DAEB1;}
    .gom-card-link {border-color:#D6AA76;cursor:pointer;}
    .gom-card-link:hover,.gom-card-link:focus-visible {background:#20323A;border-color:#F5D09D;transform:translateY(-2px);}
    .gom-card-link:focus-visible {outline:2px solid #D6AA76;outline-offset:4px;}
    [data-testid="stSidebar"],[data-testid="collapsedControl"] {display:none !important;}
    @media(max-width:800px) {.gom-grid{grid-template-columns:1fr;gap:14px}.gom-card{min-height:205px;padding:24px 18px}.gom-card-title{min-height:0}.gom-hero{padding-bottom:2rem}}
    </style>
    """)
    st.html("""
      <section class="gom-hero">
        <div class="gom-eyebrow">AN INTERACTIVE DATA INVESTIGATION · LEBANON 2023–2024</div>
        <h1 class="gom-title">The Geography of Movement</h1>
        <div class="gom-subtitle">Tracing the journeys behind Lebanon's displacement data.</div>
        <div class="gom-rule"></div>
        <p class="gom-description">Where did people move—and what can the data really tell us?</p>
      </section>
      <div class="gom-grid">
        <a class="gom-card gom-card-link" href="/chapter-1" target="_self" aria-label="Open Chapter 1, Lebanon Through Time">
          <span class="gom-num">01</span>
          <span class="gom-card-title">Lebanon Through Time</span>
          <span class="gom-card-desc">Explore the geography of reported displacement.</span>
        </a>
        <a class="gom-card gom-card-link" href="/chapter-2" target="_self" aria-label="Open Chapter 2, Trace the Journey">
          <span class="gom-num">02</span>
          <span class="gom-card-title">Trace the Journey</span>
          <span class="gom-card-desc">Discover documented origins and destinations.</span>
        </a>
        <a class="gom-card gom-card-link" href="/chapter-3" target="_self" aria-label="Open Chapter 3, The Illusion of Precision">
          <span class="gom-num">03</span>
          <span class="gom-card-title">The Illusion of Precision</span>
          <span class="gom-card-desc">Can overlapping records be added together?</span>
        </a>
      </div>
    """)


home = st.Page(homepage, title="Home", url_path="home", default=True)
chapter = st.Page("pages/01_Lebanon_Through_Time.py", title="Lebanon Through Time", url_path="chapter-1")
chapter_2 = st.Page("pages/02_Trace_the_Journey.py", title="Trace the Journey", url_path="chapter-2")
chapter_3 = st.Page("pages/03_The_Bigger_Picture.py", title="The Illusion of Precision", url_path="chapter-3")
st.session_state["gom_home_page"] = home
st.session_state["gom_chapter_1_page"] = chapter
st.session_state["gom_chapter_2_page"] = chapter_2
st.session_state["gom_chapter_3_page"] = chapter_3
st.navigation([home, chapter, chapter_2, chapter_3], position="hidden").run()
