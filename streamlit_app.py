import streamlit as st
import json
import pandas as pd
import altair as alt
from pathlib import Path
from datetime import datetime

st.set_page_config(
    page_title="PhenoExtract",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded",

)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;1,9..40,300&family=DM+Mono:wght@300;400;500&display=swap');

/* ─── GLOBAL RESET ─────────────────────────── */
*, html, body {
    font-family: 'DM Sans', sans-serif !important;
}

.stApp {
    background: #0d0f14 !important;
    color: #e2e8f0 !important;
}

/* Hide default Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding: 2.5rem 2.5rem 2rem 2.5rem !important;
    max-width: 1200px !important;
}

/* Force sidebar open, hide collapse button */
button[data-testid="collapsedControl"],
button[kind="header"] {
    display: none !important;
}
/* Hide the collapse icon text that leaks into the sidebar */
[data-testid="stSidebarCollapseButton"],
.css-1rs6os, .css-17ziqus {
    display: none !important;
}
section[data-testid="stSidebar"] span[data-icon] {
    display: none !important;
}
/* Hide any floating keyboard_double icon text */
section[data-testid="stSidebar"] button {
    display: none !important;
}
/* ─── SIDEBAR ───────────────────────────────── */
section[data-testid="stSidebar"] {
    min-width: 220px !important;
    max-width: 260px !important;
    transform: none !important;
    background: #090b10 !important;
    border-right: 1px solid #1e2433 !important;
    padding: 0 !important;
}
section[data-testid="stSidebar"] > div {
    padding: 2rem 1.5rem !important;
}

/* Sidebar brand */
.sidebar-brand {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 2.5rem;
    padding-bottom: 1.5rem;
    border-bottom: 1px solid #1e2433;
}
.sidebar-brand .logo {
    width: 36px; height: 36px;
    background: linear-gradient(135deg, #3b82f6, #8b5cf6);
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 18px;
}
.sidebar-brand .brand-name {
    font-size: 18px;
    font-weight: 700;
    color: #f1f5f9;
    letter-spacing: -0.3px;
}
.sidebar-brand .brand-sub {
    font-size: 11px;
    color: #475569;
    font-weight: 400;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}

/* Nav label */
.nav-label {
    font-size: 10px;
    font-weight: 600;
    color: #334155;
    letter-spacing: 1.2px;
    text-transform: uppercase;
    margin-bottom: 0.6rem;
}

/* Radio overrides */
div[role="radiogroup"] {
    gap: 4px !important;
    display: flex !important;
    flex-direction: column !important;

}
div[role="radiogroup"] label {
    background: transparent !important;
    border-radius: 8px !important;
    transition: all 0.15s ease !important;
    cursor: pointer !important;
    padding: 5px !important;
    width: 100% !important;
}

/* Hide the radio dot indicator (first direct div child of label) */
div[role="radiogroup"] label > div:first-of-type {
    display: none !important;
}

/* Style the text container (second direct div child of label) */
div[role="radiogroup"] label > div:last-of-type {
    font-size: 14px !important;
    font-weight: 500 !important;
    color: #94a3b8 !important;
    padding: 9px 12px !important;
    border-radius: 8px !important;
    display: flex !important;
    align-items: center !important;
    gap: 8px !important;
    transition: all 0.15s ease !important;
    background: #0d1117 !important;
    border: 1px solid #1e2433 !important;
}
div[role="radiogroup"] label:hover > div:last-of-type {
    background: #131926 !important;
    color: #93c5fd !important;
    border-color: #2d3a52 !important;
}

/* Checked state */
div[role="radiogroup"] label[data-checked="true"] > div:last-of-type {
    color: #e2e8f0 !important;
    font-weight: 600 !important;
    background: #131926 !important;
    border-color: #3b82f6 !important;
    border-left: 3px solid #3b82f6 !important;
}

/* Selectbox */
.stSelectbox > div > div {
    background: #131926 !important;
    border: 1px solid #1e2433 !important;
    border-radius: 10px !important;
    cursor: pointer !important;
    color: #e2e8f0 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 13px !important;
}
.stSelectbox label {
    font-size: 11px !important;
    font-weight: 600 !important;
    color: #334155 !important;
    letter-spacing: 0.8px !important;
    text-transform: uppercase !important;
    margin-top: 1.5rem !important;
}

/* ─── PAGE TITLE ─────────────────────────────── */
.page-header {
    margin-bottom: 2rem;
}
.page-header .eyebrow {
    font-size: 11px;
    font-weight: 600;
    color: #3b82f6;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 6px;
}
.page-header h1 {
    font-size: 2rem !important;
    font-weight: 700 !important;
    color: #f1f5f9 !important;
    letter-spacing: -0.8px !important;
    line-height: 1.2 !important;
    margin: 0 0 8px 0 !important;
}
.page-header .subtitle {
    font-size: 14px;
    color: #475569;
    font-weight: 400;
}

/* ─── METRIC CARDS ──────────────────────────── */
.metrics-row {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
    margin-bottom: 1rem;
}
.metric-card {
    background: #0f1520;
    border: 1px solid #1e2433;
    border-radius: 14px;
    padding: 1.4rem 1.6rem;
    position: relative;
    overflow: hidden;
    transition: border-color 0.2s ease;
}
.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #3b82f6, #8b5cf6);
    opacity: 0;
    transition: opacity 0.2s ease;
}
.metric-card:hover { border-color: #2d3a52; }
.metric-card:hover::before { opacity: 1; }
.metric-card .label {
    font-size: 11px;
    font-weight: 600;
    color: #334155;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 10px;
}
.metric-card .value {
    font-size: 2.2rem;
    font-weight: 700;
    color: #f1f5f9;
    letter-spacing: -1px;
    font-family: 'DM Mono', monospace !important;
    line-height: 1;
}
.metric-card .value span {
    font-size: 1rem;
    font-weight: 400;
    color: #475569;
    margin-left: 2px;
}
.metric-card .sub {
    font-size: 12px;
    color: #3b82f6;
    margin-top: 8px;
    font-weight: 500;
}

/* ─── SECTION HEADERS ───────────────────────── */
.section-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin: 2rem 0 1rem 0;
}
.section-header .dot {
    width: 6px; height: 6px;
    background: #3b82f6;
    border-radius: 50%;
    flex-shrink: 0;
}
.section-header h3 {
    font-size: 13px !important;
    font-weight: 600 !important;
    color: #64748b !important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
    margin: 0 !important;
}
.section-header .line {
    flex: 1;
    height: 1px;
    background: #1e2433;
}

/* ─── DATAFRAME ─────────────────────────────── */
.stDataFrame {
    border-radius: 12px !important;
    overflow: hidden !important;
    border: 1px solid #1e2433 !important;
}
.stDataFrame [data-testid="stDataFrameResizable"] {
    background: #0f1520 !important;
}
iframe {
    border-radius: 12px !important;
}

/* ─── CLINICAL NOTE ─────────────────────────── */
.note-container {
    background: #090b10;
    border: 1px solid #1e2433;
    border-radius: 14px;
    padding: 1.5rem;
    height: 260px;
    overflow-y: auto;
    font-family: 'DM Mono', monospace;
    font-size: 13px;
    line-height: 1.8;
    color: #94a3b8;
    letter-spacing: 0.2px;
    position: relative;
}
.note-container::-webkit-scrollbar { width: 4px; }
.note-container::-webkit-scrollbar-track { background: transparent; }
.note-container::-webkit-scrollbar-thumb { background: #1e2433; border-radius: 4px; }
.note-label {
    font-size: 10px;
    font-weight: 600;
    color: #1e40af;
    background: #1e3a5f22;
    border: 1px solid #1e40af44;
    border-radius: 6px;
    padding: 2px 8px;
    display: inline-block;
    margin-bottom: 1rem;
    letter-spacing: 0.8px;
    text-transform: uppercase;
}

/* ─── CASE METRICS ──────────────────────────── */
.case-metrics {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
}
.case-metric {
    background: #0f1520;
    border: 1px solid #1e2433;
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
    text-align: center;
}
.case-metric .cm-label {
    font-size: 11px;
    color: #334155;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin-bottom: 8px;
}
.case-metric .cm-value {
    font-size: 1.8rem;
    font-weight: 700;
    font-family: 'DM Mono', monospace !important;
    letter-spacing: -0.5px;
}
.cm-value.f1 { color: #3b82f6; }
.cm-value.precision { color: #8b5cf6; }
.cm-value.recall { color: #10b981; }

/* ─── ABOUT PAGE ─────────────────────────────── */
.about-card {
    background: #0f1520;
    border: 1px solid #1e2433;
    border-radius: 16px;
    padding: 2rem;
    margin-bottom: 1.2rem;
}
.about-card h3 {
    font-size: 14px !important;
    font-weight: 600 !important;
    color: #94a3b8 !important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
    margin-bottom: 1rem !important;
}
.about-card p {
    font-size: 15px;
    color: #64748b;
    line-height: 1.7;
    margin: 0 0 0.8rem 0;
}
.about-card .tag {
    display: inline-block;
    background: #131926;
    border: 1px solid #1e2433;
    border-radius: 6px;
    font-size: 12px;
    font-family: 'DM Mono', monospace;
    color: #3b82f6;
    padding: 3px 10px;
    margin: 3px 3px 3px 0;
}

/* ─── BADGE ─────────────────────────────────── */
.badge {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    background: #0f2040;
    border: 1px solid #1e3a6e;
    border-radius: 20px;
    padding: 4px 12px;
    font-size: 12px;
    color: #60a5fa;
    font-weight: 500;
    margin-bottom: 1.5rem;
}

/* ─── CHART ─────────────────────────────────── */
.stBarChart > div {
    background: transparent !important;
}

/* ─── DIVIDER ───────────────────────────────── */
hr {
    border: none !important;
    border-top: 1px solid #1e2433 !important;
    margin: 2rem 0 !important;
}
/* ─── DOWNLOAD BUTTON ───────────────────────── */
.stDownloadButton > button {
    color: #000000 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    border-radius: 10px !important;
    transition: all 0.2s ease !important;
}
.stDownloadButton > button p,
.stDownloadButton > button span,
.stDownloadButton > button div {
    color: #000000 !important;
}
/* Streamlit native metric */
[data-testid="metric-container"] {
    background: #0f1520 !important;
    border: 1px solid #1e2433 !important;
    border-radius: 12px !important;
    padding: 1.2rem !important;
}
[data-testid="stMetricValue"] {
    font-family: 'DM Mono', monospace !important;
    color: #f1f5f9 !important;
}
[data-testid="stMetricLabel"] {
    color: #475569 !important;
    font-size: 12px !important;
    text-transform: uppercase !important;
    letter-spacing: 0.8px !important;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# 0. PATHS
# ─────────────────────────────────────────────
DATA_DIR = Path("data")
RESOURCES_DIR = Path("resources/clinical_notes")

A_PATH = DATA_DIR / "moduleA_output.json"
B_PATH = DATA_DIR / "moduleB_output.json"
GOLD_PATH = DATA_DIR / "gold.json"


# ─────────────────────────────────────────────
# 1. LOAD DATA
# ─────────────────────────────────────────────
with open(A_PATH, "r") as f:
    moduleA = json.load(f)
with open(B_PATH, "r") as f:
    moduleB = json.load(f)
with open(GOLD_PATH, "r") as f:
    gold_data = json.load(f)

A_dict = {case["case_id"]: case for case in moduleA}
B_dict = {case["case_id"]: case for case in moduleB}
GOLD_dict = {case["case_id"]: case for case in gold_data}


# ─────────────────────────────────────────────
# 2. UTILITY FUNCTIONS
# ─────────────────────────────────────────────
def load_clinical_note(case_id):
    file_path = RESOURCES_DIR / f"{case_id}.txt"
    return file_path.read_text() if file_path.exists() else "No clinical note available."


def extract_gold_surfaces(gold_case):
    if isinstance(gold_case, list):
        return {str(x).lower() for x in gold_case}
    if "excluded" in gold_case:
        excluded = gold_case["excluded"]
        if isinstance(excluded, list):
            if excluded and isinstance(excluded[0], str):
                return {x.lower() for x in excluded}
            if excluded and isinstance(excluded[0], dict):
                return {x["surface"].lower() for x in excluded}
    if "excluded_mentions" in gold_case:
        return {m["surface"].lower() for m in gold_case["excluded_mentions"]}
    return set()


def compute_case_metrics(case_id):
    pred = {m["surface"].lower() for m in B_dict[case_id]["excluded_mentions"]}
    gold = extract_gold_surfaces(GOLD_dict[case_id])
    TP = len(pred & gold)
    FP = len(pred - gold)
    FN = len(gold - pred)
    precision = TP / (TP + FP) if (TP + FP) else 0
    recall    = TP / (TP + FN) if (TP + FN) else 0
    f1        = (2 * precision * recall) / (precision + recall) if (precision + recall) else 0
    return TP, FP, FN, precision, recall, f1


def compute_global_metrics():
    rows = []
    for case_id in A_dict:
        TP, FP, FN, P, R, F1 = compute_case_metrics(case_id)
        rows.append({"case_id": case_id, "TP": TP, "FP": FP, "FN": FN, "P": P, "R": R, "F1": F1})
    df = pd.DataFrame(rows)
    macro = {"precision": df["P"].mean(), "recall": df["R"].mean(), "f1": df["F1"].mean()}
    total_TP = df["TP"].sum(); total_FP = df["FP"].sum(); total_FN = df["FN"].sum()
    mp = total_TP / (total_TP + total_FP) if (total_TP + total_FP) else 0
    mr = total_TP / (total_TP + total_FN) if (total_TP + total_FN) else 0
    mf = (2 * mp * mr) / (mp + mr) if (mp + mr) else 0
    micro = {"precision": mp, "recall": mr, "f1": mf}
    return df, macro, micro


# ─────────────────────────────────────────────
# 3. SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <div class="logo">🧬</div>
        <div>
            <div class="brand-name">PhenoExtract</div>
            <div class="brand-sub">HPO · NLP · Eval</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="nav-label">Navigation</div>', unsafe_allow_html=True)

    page = st.radio(
        label="",
        options=[ "Case Viewer", "Evaluation Dashboard","About the Project"],
        label_visibility="collapsed"
    )

    if page == "Case Viewer":
        st.markdown("<br>", unsafe_allow_html=True)
        case_ids = sorted(list(A_dict.keys()))
        selected_case = st.selectbox("Select Case", case_ids)
    else:
        selected_case = None

    # Sidebar footer
    st.markdown("""
    <div style='margin-top:3rem; padding-top:1.5rem; border-top:1px solid #1e2433;'>
        <div style='font-size:11px; color:#1e2433; text-align:center; font-family: DM Mono, monospace;'>
            v1.0 · Phenopacket-ready
        </div>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# 4. PAGE ROUTING
# ─────────────────────────────────────────────
if page == "Evaluation Dashboard":
    df, macro, micro = compute_global_metrics()

    st.markdown("""
    <div class="page-header">
        <div class="eyebrow">System Performance</div>
        <h1>Evaluation Dashboard</h1>
        <div class="subtitle">Negation extraction accuracy across all cases</div>
    </div>
    """, unsafe_allow_html=True)

    # Per-case table
    st.markdown("""
    <div class="section-header" style="margin-top:2rem;">
        <div class="dot" style="background:#10b981; color:#000000"></div>
        <h3>Per-Case Breakdown</h3>
        <div class="line"></div>
    </div>
    """, unsafe_allow_html=True)

    styled_df = df.style.format({"P": "{:.3f}", "R": "{:.3f}", "F1": "{:.3f}"})
    st.dataframe(styled_df, use_container_width=True, hide_index=True)
    # Micro metrics
    st.markdown("""
    <div class="section-header">
        <div class="dot"></div>
        <h3>Micro-Averaged</h3>       
        <div class="line"></div>
    </div>
    <p>Micro scores show how well the system does overall across all cases combined.</p>
    <div class="metrics-row">
        <div class="metric-card">
            <div class="label">F1 Score</div>
            <div class="value">{f1}<span>/ 1.0</span></div>
            <div class="sub">↑ Harmonic mean</div>
        </div>
        <div class="metric-card">
            <div class="label">Precision</div>
            <div class="value">{p}<span>/ 1.0</span></div>
            <div class="sub">TP / (TP + FP)</div>
        </div>
        <div class="metric-card">
            <div class="label">Recall</div>
            <div class="value">{r}<span>/ 1.0</span></div>
            <div class="sub">TP / (TP + FN)</div>
        </div>
    </div>
    """.format(
        f1=f"{micro['f1']:.3f}",
        p=f"{micro['precision']:.3f}",
        r=f"{micro['recall']:.3f}"
    ), unsafe_allow_html=True)

    # Macro metrics
    st.markdown("""
    <div class="section-header" style="margin-top:1.5rem;">
        <div class="dot" style="background:#8b5cf6;"></div>
        <h3>Macro-Averaged</h3>
        <div class="line"></div>
    </div>
    <p>Macro scores show how well the system does on an average case.</p>
    <div class="metrics-row">
        <div class="metric-card">
            <div class="label">F1 Score</div>
            <div class="value" style="color:#a78bfa;">{f1}<span>/ 1.0</span></div>
            <div class="sub" style="color:#8b5cf6;">↑ Per-case avg</div>
        </div>
        <div class="metric-card">
            <div class="label">Precision</div>
            <div class="value" style="color:#a78bfa;">{p}<span>/ 1.0</span></div>
            <div class="sub" style="color:#8b5cf6;">Per-case avg</div>
        </div>
        <div class="metric-card">
            <div class="label">Recall</div>
            <div class="value" style="color:#a78bfa;">{r}<span>/ 1.0</span></div>
            <div class="sub" style="color:#8b5cf6;">Per-case avg</div>
        </div>
    </div>
    """.format(
        f1=f"{macro['f1']:.3f}",
        p=f"{macro['precision']:.3f}",
        r=f"{macro['recall']:.3f}"
    ), unsafe_allow_html=True)

    

    # ── Interactive Scatter: Precision vs Recall ──
    st.markdown("""
    <div class="section-header" style="margin-top:2rem;">
        <div class="dot" style="background:#f59e0b;"></div>
        <h3>Precision vs Recall</h3>
        <div class="line"></div>
    </div>
    """, unsafe_allow_html=True)

    scatter = alt.Chart(df).mark_circle(stroke="#1e2433", strokeWidth=1).encode(
        x=alt.X("P:Q", title="Precision", scale=alt.Scale(domain=[0, 1])),
        y=alt.Y("R:Q", title="Recall", scale=alt.Scale(domain=[0, 1])),
        color=alt.Color("F1:Q", scale=alt.Scale(scheme="viridis"), legend=alt.Legend(title="F1")),
        size=alt.Size("TP:Q", scale=alt.Scale(range=[80, 500]), legend=alt.Legend(title="TP Count")),
        tooltip=[
            alt.Tooltip("case_id:N", title="Case"),
            alt.Tooltip("F1:Q", title="F1", format=".3f"),
            alt.Tooltip("P:Q", title="Precision", format=".3f"),
            alt.Tooltip("R:Q", title="Recall", format=".3f"),
            alt.Tooltip("TP:Q", title="TP"),
            alt.Tooltip("FP:Q", title="FP"),
            alt.Tooltip("FN:Q", title="FN"),
        ],
    ).properties(height=340).configure_view(
        fill="#0f1520", stroke=None
    ).configure_axis(
        gridColor="#1e2433", domainColor="#334155",
        labelColor="#64748b", titleColor="#94a3b8"
    ).configure_legend(
        labelColor="#94a3b8", titleColor="#94a3b8"
    ).interactive()

    st.altair_chart(scatter, use_container_width=True, theme=None)

    # ── Grouped Bar: F1 / Precision / Recall per case ──
    st.markdown("""
    <div class="section-header" style="margin-top:2rem;">
        <div class="dot" style="background:#3b82f6;"></div>
        <h3>Per-Case Metrics Comparison</h3>
        <div class="line"></div>
    </div>
    """, unsafe_allow_html=True)

    bar_data = df.melt(id_vars="case_id", value_vars=["F1", "P", "R"],
                       var_name="Metric", value_name="Score")
    bar_data["Metric"] = bar_data["Metric"].map({"F1": "F1 Score", "P": "Precision", "R": "Recall"})
    grouped_bar = alt.Chart(bar_data).mark_bar(cornerRadiusTopLeft=3, cornerRadiusTopRight=3).encode(
        x=alt.X("case_id:N", title=None, axis=alt.Axis(labelAngle=-45)),
        xOffset=alt.XOffset("Metric:N"),
        y=alt.Y("Score:Q", title="Score", scale=alt.Scale(domain=[0, 1])),
        color=alt.Color("Metric:N", scale=alt.Scale(
            domain=["F1 Score", "Precision", "Recall"],
            range=["#3b82f6", "#8b5cf6", "#10b981"]
        )),
        tooltip=[
            alt.Tooltip("case_id:N", title="Case"),
            alt.Tooltip("Metric:N"),
            alt.Tooltip("Score:Q", format=".3f"),
        ],
    ).properties(height=340).configure_view(
        fill="#0f1520", stroke=None
    ).configure_axis(
        gridColor="#1e2433", domainColor="#334155",
        labelColor="#94a3b8", titleColor="#94a3b8"
    ).configure_legend(
        labelColor="#94a3b8", titleColor="#94a3b8"
    )

    st.altair_chart(grouped_bar, use_container_width=True, theme=None)


# ─────────────────────────────────────────────
# 5. CASE VIEWER
# ─────────────────────────────────────────────
elif page == "Case Viewer":
    case_id = selected_case or (sorted(list(A_dict.keys()))[0] if A_dict else None)
    if not case_id:
        st.warning("No cases available.")
        st.stop()
    TP, FP, FN, P, R, F1 = compute_case_metrics(case_id)
    st.markdown(f"""
    <div class="page-header">
        <div class="eyebrow">Case Viewer</div>
        <h1>{case_id}</h1>
        <div class="subtitle">Clinical note analysis · HPO mapping · Negation extraction</div>
    </div>
    """, unsafe_allow_html=True)

    # Clinical note
    st.markdown("""
    <div class="section-header">
        <div class="dot"></div>
        <h3>Clinical Note</h3>
        <div class="line"></div>
    </div>
    """, unsafe_allow_html=True)

    note_text = load_clinical_note(case_id)
    st.markdown(f"""
    <div class="note-container">
        <div class="note-label">📋 raw note</div>
        <pre style='margin:0; font-family: inherit; white-space: pre-wrap; word-wrap: break-word;'>{note_text}</pre>
    </div>
    """, unsafe_allow_html=True)

    # ── Export buttons right under clinical note ──
    def build_phenopacket(cid):
        """Build a GA4GH Phenopacket v2 JSON for the given case."""
        features = []
        for m in A_dict[cid]["mapped_exclusions"]:
            top = m["hpo_matches"][0]
            if top["hpo_id"]:
                features.append({
                    "type": {
                        "id": top["hpo_id"],
                        "label": top["label"]
                    },
                    "excluded": True,
                    "description": f"Negated mention: '{m['surface']}'"
                })
        return {
            "id": f"phenopacket-{cid}",
            "subject": {"id": cid},
            "phenotypicFeatures": features,
            "metaData": {
                "created": datetime.utcnow().isoformat() + "Z",
                "createdBy": "PhenoExtract",
                "phenopacketSchemaVersion": "2.0",
                "resources": [{
                    "id": "hp",
                    "name": "Human Phenotype Ontology",
                    "url": "http://purl.obolibrary.org/obo/hp.owl",
                    "version": "2024-08-13",
                    "namespacePrefix": "HP",
                    "iriPrefix": "http://purl.obolibrary.org/obo/HP_"
                }]
            }
        }

    def build_fhir_bundle(cid):
        """Build an HL7 FHIR R4 Observation Bundle for the given case."""
        entries = []
        for i, m in enumerate(A_dict[cid]["mapped_exclusions"]):
            top = m["hpo_matches"][0]
            coding = []
            if top["hpo_id"]:
                coding.append({
                    "system": "http://purl.obolibrary.org/obo/hp.owl",
                    "code": top["hpo_id"],
                    "display": top["label"]
                })
            entries.append({
                "fullUrl": f"urn:uuid:obs-{cid}-{i}",
                "resource": {
                    "resourceType": "Observation",
                    "id": f"obs-{cid}-{i}",
                    "status": "final",
                    "code": {
                        "coding": coding,
                        "text": m["surface"]
                    },
                    "subject": {"reference": f"Patient/{cid}"},
                    "interpretation": [{
                        "coding": [{
                            "system": "http://terminology.hl7.org/CodeSystem/v3-ObservationInterpretation",
                            "code": "NEG",
                            "display": "Negative"
                        }],
                        "text": "Explicitly excluded / negated"
                    }],
                    "valueCodeableConcept": {
                        "coding": coding,
                        "text": f"Absent: {m['surface']}"
                    }
                }
            })
        return {
            "resourceType": "Bundle",
            "id": f"fhir-bundle-{cid}",
            "type": "collection",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "entry": entries
        }

    pp_json = json.dumps(build_phenopacket(case_id), indent=2)
    st.download_button(
        label="⬇  Download GA4GH Phenopacket v2 JSON",
        data=pp_json,
        file_name=f"{case_id}_phenopacket.json",
        mime="application/json",
        use_container_width=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # HPO Mapping — full width
    st.markdown("""
    <div class="section-header">
        <div class="dot" style="background:#090b10;"></div>
        <h3>HPO Mapping</h3>
        <div class="line"></div>
    </div>
    """, unsafe_allow_html=True)

    rows = []
    for m in A_dict[case_id]["mapped_exclusions"]:
        top = m["hpo_matches"][0]
        rows.append({
            "Explicit Exclusions": m["surface"],
            "HPO ID": top["hpo_id"],
            "Label": top["label"],
            "Match": top["match_type"]
        })
    df_A = pd.DataFrame(rows)
    st.dataframe(df_A, use_container_width=True, hide_index=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Excluded Findings — full width
    st.markdown("""
    <div class="section-header">
        <div class="dot" style="background:#10b981;"></div>
        <h3>Excluded Findings</h3>
        <div class="line"></div>
    </div>
    """, unsafe_allow_html=True)

    clean_rows = []
    for m in B_dict[case_id]["excluded_mentions"]:
        clean_rows.append({
            "Explicit Exclusions": m.get("surface"),
            "Negation Cue": m.get("negation_cue"),
            "Evidence": m.get("evidence", {}).get("snippet", ""),
            "Context": m.get("context", "")
        })
    df_B = pd.DataFrame(clean_rows)
    st.dataframe(df_B, use_container_width=True, hide_index=True)

    # Top metrics
    st.markdown(f"""
    <div class="case-metrics">
        <div class="case-metric">
            <div class="cm-label">F1 Score</div>
            <div class="cm-value f1">{F1:.3f}</div>
        </div>
        <div class="case-metric">
            <div class="cm-label">Precision</div>
            <div class="cm-value precision">{P:.3f}</div>
        </div>
        <div class="case-metric">
            <div class="cm-label">Recall</div>
            <div class="cm-value recall">{R:.3f}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # TP/FP/FN badges
    st.markdown(f"""
    <div style="display:flex; gap:8px; margin: 1rem 0 2rem 0;">
        <div style="background:#0f2d20; border:1px solid #10b981; border-radius:20px; padding:4px 14px; font-size:12px; color:#10b981; font-family:'DM Mono',monospace;">
            TP · {TP}
        </div>
        <div style="background:#2d1515; border:1px solid #ef4444; border-radius:20px; padding:4px 14px; font-size:12px; color:#f87171; font-family:'DM Mono',monospace;">
            FP · {FP}
        </div>
        <div style="background:#2d2010; border:1px solid #f59e0b; border-radius:20px; padding:4px 14px; font-size:12px; color:#fbbf24; font-family:'DM Mono',monospace;">
            FN · {FN}
        </div>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 6. ABOUT
# ─────────────────────────────────────────────
elif page == "About the Project":
    st.markdown("""
    <div class="page-header">
        <div class="eyebrow">Documentation</div>
        <h1>About This Project</h1>
        <div class="subtitle">Automated phenotype extraction from unstructured clinical notes</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="about-card">
        <h3>Overview</h3>
        <p>
            This pipeline automatically extracts <strong style="color:#e2e8f0;">explicitly excluded clinical findings</strong> from messy medical notes, 
            maps them to standardized <strong style="color:#e2e8f0;">HPO terms</strong>, and evaluates extraction quality across cases. 
            It transforms free-text into structured, <strong style="color:#e2e8f0;">phenopacket-ready data</strong> to support faster and more accurate rare-disease diagnosis.
        </p>
    </div>

    <div class="about-card">
        <h3>Pipeline Modules</h3>
        <p><strong style="color:#e2e8f0;">Module 1 — Negation Extractor</strong></p>
        <p>Detects negated symptom mentions using context-aware NLP. Captures evidence sentences and outputs structured exclusion records with span-level precision.</p>
        <div style="margin: 0.8rem 0 1.2rem 0;">
            <span class="tag">negation_cue</span>
            <span class="tag">evidence_snippet</span>
            <span class="tag">span_offset</span>
        </div>
        <p><strong style="color:#e2e8f0;">Module 2 — HPO Mapper</strong></p>
        <p>Maps extracted exclusions to standardized HPO term IDs using a hybrid exact + fuzzy lexical matching strategy for maximum coverage.</p>
        <div style="margin: 0.8rem 0 0 0;">
            <span class="tag">exact_match</span>
            <span class="tag">fuzzy_match</span>
            <span class="tag">hpo_id</span>
        </div>
    </div>

    <div class="about-card">
        <h3>Evaluation</h3>
        <p>
            System performance is measured against gold-standard annotations using 
            token-level Precision, Recall, and F1 across both 
            <strong style="color:#e2e8f0;">micro</strong> and 
            <strong style="color:#e2e8f0;">macro</strong> averaging strategies.
        </p>
        <div style="margin-top:0.8rem;">
            <span class="tag">micro_avg</span>
            <span class="tag">macro_avg</span>
            <span class="tag">per-case_breakdown</span>
        </div>
    </div>
    """, unsafe_allow_html=True)