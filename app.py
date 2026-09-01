from __future__ import annotations

import os
import sys
import logging
from pathlib import Path

import pandas as pd
import streamlit as st
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent
sys.path.append(str(ROOT / "src"))

from case_loader import load_cases, load_evidence
from review_manager import load_reviews, save_review, make_demo_reviews
from rule_checker import run_checks
from validators import evidence_status, validate_case_csv, validate_evidence_csv, validate_review_csv

LOGGER = logging.getLogger("netsage_ai")

load_dotenv(ROOT / ".env")

DATA = ROOT / "data" / "cases.csv"
REVIEWS = ROOT / "data" / "review_log.csv"
EVIDENCE = ROOT / "data" / "evidence.csv"

st.set_page_config(page_title="NetSage AI", page_icon="🛜", layout="wide")

st.markdown(
    """
    <style>
    :root {
        --bg: #0b1220;
        --bg-2: #0f1a2b;
        --sidebar: #101b2d;
        --panel: #121f31;
        --panel-alt: #17273d;
        --panel-soft: #0e1727;
        --border: #24364a;
        --border-soft: #1b2d42;
        --text: #eaf3ff;
        --text-soft: #9bb0c8;
        --heading: #f4f8ff;
        --primary: #4aa3ff;
        --primary-soft: rgba(74, 163, 255, 0.12);
        --success: #38d39f;
        --success-soft: rgba(56, 211, 159, 0.12);
        --reference: #67d2ff;
        --reference-soft: rgba(103, 210, 255, 0.12);
        --warning: #f4b454;
        --warning-soft: rgba(244, 180, 84, 0.12);
        --danger: #ff6d7a;
        --danger-soft: rgba(255, 109, 122, 0.12);
        --chip: #15263b;
        --shadow: rgba(2, 6, 23, 0.45);
    }

    html, body, .stApp, [data-testid="stAppViewContainer"] {
        background: linear-gradient(180deg, var(--bg) 0%, var(--bg-2) 100%);
        color: var(--text);
        font-family: "Inter", "Segoe UI", sans-serif;
    }

    .block-container {
        padding-top: 1.2rem;
        padding-bottom: 2rem;
        max-width: 1500px;
    }

    h1, h2, h3, h4, h5, h6 {
        color: var(--heading) !important;
        letter-spacing: -0.03em;
        margin-top: 0 !important;
    }

    h1 {
        font-size: 2.25rem !important;
        font-weight: 800 !important;
        margin-bottom: 0.25rem !important;
    }

    h2 {
        font-size: 1.5rem !important;
        font-weight: 700 !important;
        margin-bottom: 0.6rem !important;
    }

    h3 {
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        margin-bottom: 0.5rem !important;
    }

    p, li, label, .stMarkdown, .stCaption {
        color: var(--text-soft);
        line-height: 1.6;
    }

    a {
        color: var(--reference) !important;
        text-decoration: none !important;
    }

    a:hover {
        text-decoration: underline !important;
    }

    [data-testid="stSidebar"] {
        background: rgba(14, 23, 39, 0.96);
        border-right: 1px solid var(--border);
    }

    [data-testid="stSidebar"] .block-container {
        padding: 1.2rem 0.9rem;
    }

    [data-testid="stTabs"] {
        border-bottom: 1px solid var(--border);
        margin-bottom: 1.25rem;
        overflow: visible;
    }

    [data-testid="stTabs"] [role="tablist"] {
        gap: 0.7rem;
        padding-left: 0.15rem;
    }

    [data-testid="stTabs"] [role="tab"] {
        background: transparent !important;
        border: 1px solid transparent !important;
        border-radius: 10px 10px 0 0 !important;
        color: var(--text-soft) !important;
        font-weight: 700 !important;
        padding: 0.7rem 1rem !important;
        font-size: 0.9rem !important;
        transition: all 0.2s ease;
    }

    [data-testid="stTabs"] [role="tab"]:hover {
        border-color: var(--border) !important;
        color: var(--heading) !important;
    }

    [data-testid="stTabs"] [role="tab"][aria-selected="true"] {
        background: rgba(74, 163, 255, 0.08) !important;
        border-color: var(--primary) !important;
        border-bottom-color: transparent !important;
        color: var(--heading) !important;
        box-shadow: inset 0 -2px 0 var(--primary);
    }

    [data-testid="stMetric"] {
        background: linear-gradient(180deg, rgba(18, 31, 49, 0.95), rgba(15, 26, 43, 0.95));
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 1rem 1rem 0.9rem;
        box-shadow: 0 8px 18px var(--shadow);
    }

    [data-testid="stMetricLabel"] {
        color: var(--text-soft) !important;
        font-size: 0.7rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.1em !important;
        text-transform: uppercase;
    }

    [data-testid="stMetricValue"] {
        color: var(--heading) !important;
        font-size: 1.65rem !important;
        font-weight: 800 !important;
    }

    .stDataFrame, .stDataFrame > div {
        background: rgba(18, 31, 49, 0.9);
        border: 1px solid var(--border);
        border-radius: 12px;
        overflow: hidden;
    }

    .stDataFrame th {
        background: rgba(21, 38, 59, 0.95);
        color: var(--heading) !important;
        font-size: 0.72rem !important;
        font-weight: 800 !important;
        letter-spacing: 0.08em !important;
        text-transform: uppercase;
    }

    .stDataFrame td {
        color: var(--text);
        border-top: 1px solid var(--border);
    }

    input, textarea, div[data-baseweb="select"] > div, .stNumberInput > div, .stTextInput > div {
        background: rgba(18, 31, 49, 0.9) !important;
        color: var(--text) !important;
        border: 1px solid var(--border) !important;
        border-radius: 10px !important;
    }

    button, button[kind="primary"] {
        border-radius: 10px !important;
        border: 1px solid var(--border) !important;
        font-weight: 700 !important;
        transition: transform 0.18s ease, box-shadow 0.18s ease, opacity 0.18s ease;
    }

    button:hover {
        transform: translateY(-1px);
        box-shadow: 0 8px 18px rgba(0, 0, 0, 0.18);
    }

    button[kind="primary"], button[data-testid="baseButton-primary"] {
        background: linear-gradient(180deg, #4aa3ff 0%, #2c7ae8 100%) !important;
        border-color: rgba(74, 163, 255, 0.7) !important;
        color: white !important;
    }

    [data-testid="stAlert"] {
        border-radius: 12px;
        border-left: 4px solid var(--primary);
        background: rgba(22, 38, 58, 0.9);
        color: var(--text);
    }

    .stCodeBlock {
        background: rgba(8, 15, 25, 0.9);
        border: 1px solid var(--border);
        border-radius: 12px;
    }

    .brand-shell {
        background: linear-gradient(180deg, rgba(17, 31, 49, 0.92), rgba(12, 22, 35, 0.92));
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 1.1rem 1.25rem;
        margin-bottom: 1.2rem;
        box-shadow: 0 14px 30px var(--shadow);
    }

    .brand-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 1rem;
    }

    .case-selector {
        background: rgba(11, 18, 32, 0.7);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 1rem 1.1rem;
    }

    .selector-label {
        color: var(--text-soft);
        font-size: 0.72rem;
        font-weight: 800;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        margin-bottom: 0.5rem;
    }

    .selector-id {
        color: var(--heading);
        font-size: 2rem;
        font-weight: 800;
        letter-spacing: -0.05em;
        margin-bottom: 0.2rem;
    }

    .selector-symptom {
        color: var(--text);
        font-size: 1rem;
        font-weight: 600;
        line-height: 1.5;
    }

    .case-meta-grid {
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: 0.7rem;
        margin-top: 1rem;
    }

    .meta-chip {
        background: rgba(21, 38, 59, 0.9);
        border: 1px solid var(--border);
        border-radius: 10px;
        padding: 0.7rem 0.8rem;
    }

    .meta-chip .kicker {
        display: block;
        color: var(--text-soft);
        font-size: 0.66rem;
        font-weight: 800;
        letter-spacing: 0.09em;
        margin-bottom: 0.38rem;
        text-transform: uppercase;
    }

    .meta-chip .value {
        display: block;
        color: var(--heading);
        font-size: 0.94rem;
        font-weight: 700;
    }

    .brand-title {
        font-size: 2rem;
        font-weight: 800;
        letter-spacing: -0.06em;
        color: var(--heading);
        margin: 0;
    }

    .brand-subtitle {
        margin: 0.2rem 0 0;
        color: var(--text-soft);
        font-size: 0.95rem;
    }

    .status-pill {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: rgba(56, 211, 159, 0.08);
        color: var(--success);
        border: 1px solid rgba(56, 211, 159, 0.35);
        border-radius: 999px;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        padding: 0.38rem 0.7rem;
    }

    .status-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: var(--success);
        box-shadow: 0 0 12px rgba(56, 211, 159, 0.8);
    }

    .workspace-panel {
        background: rgba(18, 31, 49, 0.9);
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 1.1rem;
        margin-bottom: 1.1rem;
        box-shadow: 0 10px 24px rgba(0, 0, 0, 0.18);
    }

    .panel-kicker {
        color: var(--text-soft);
        font-size: 0.7rem;
        font-weight: 800;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        margin-bottom: 0.7rem;
    }

    .workflow-strip {
        display: flex;
        flex-wrap: wrap;
        gap: 0.55rem;
        align-items: center;
        margin: 0.8rem 0 0.1rem;
    }

    .workflow-step {
        background: rgba(21, 38, 59, 0.9);
        border: 1px solid var(--border);
        border-radius: 999px;
        color: var(--heading);
        padding: 0.4rem 0.75rem;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }

    .workflow-arrow {
        color: var(--text-soft);
        font-weight: 700;
        font-size: 0.9rem;
    }

    .feature-grid {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 0.8rem;
        margin-top: 0.8rem;
    }

    .info-card {
        background: rgba(18, 31, 49, 0.9);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 1rem;
        min-height: 100%;
    }

    .detail-label {
        color: var(--text-soft);
        display: block;
        font-size: 0.7rem;
        font-weight: 800;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        margin-bottom: 0.5rem;
    }

    .detail-value {
        color: var(--heading);
        display: block;
        font-size: 1.05rem;
        font-weight: 700;
        line-height: 1.45;
    }

    .badge {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        border-radius: 999px;
        padding: 0.3rem 0.7rem;
        font-size: 0.68rem;
        font-weight: 800;
        letter-spacing: 0.09em;
        text-transform: uppercase;
        border: 1px solid transparent;
    }

    .badge-verified {
        background: var(--success-soft);
        color: var(--success);
        border-color: rgba(56, 211, 159, 0.45);
    }

    .badge-reference {
        background: var(--reference-soft);
        color: var(--reference);
        border-color: rgba(103, 210, 255, 0.45);
    }

    .badge-pending {
        background: var(--warning-soft);
        color: var(--warning);
        border-color: rgba(244, 180, 84, 0.45);
    }

    .badge-danger {
        background: var(--danger-soft);
        color: var(--danger);
        border-color: rgba(255, 109, 122, 0.45);
    }

    .sidebar-brief {
        background: rgba(14, 22, 35, 0.8);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 0.7rem 0.8rem;
        margin: 0.5rem 0 0.8rem;
    }

    .sidebar-brief strong {
        color: var(--heading);
        font-size: 0.74rem;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }

    .small-metric {
        font-size: 0.76rem;
        color: var(--text-soft);
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-bottom: 0.2rem;
    }

    .small-value {
        font-size: 1.35rem;
        font-weight: 800;
        color: var(--heading);
        line-height: 1.2;
    }

    .distribution-bar {
        display: flex;
        height: 11px;
        border-radius: 999px;
        overflow: hidden;
        background: rgba(255, 255, 255, 0.06);
        border: 1px solid var(--border);
        margin-top: 0.5rem;
    }

    .distribution-segment {
        height: 100%;
        display: block;
    }

    .segment-verified { background: var(--success); }
    .segment-reference { background: var(--reference); }
    .segment-pending { background: var(--warning); }

    @media (max-width: 1100px) {
        .feature-grid { grid-template-columns: 1fr 1fr; }
    }

    @media (max-width: 820px) {
        .feature-grid { grid-template-columns: 1fr; }
        .brand-row { flex-direction: column; align-items: flex-start; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def status_card(status: str, detail: str) -> str:
    css_status = status.lower()
    return f'<div class="status-card status-{css_status}"><strong>{status}</strong><span>{detail}</span></div>'


def render_badge(status: str) -> str:
    """Render a status badge with consistent styling."""
    css_class = status.lower().replace(" ", "-")
    return f'<span class="badge badge-{css_class}">{status}</span>'


def finding_card(result: dict) -> str:
    status = str(result["status"]).lower()
    symbol = "✓" if status == "pass" else "⚠" if status == "warn" else "✕"
    return (
        f'<div class="finding finding-{status}"><div class="finding-title">{symbol} '
        f'{result["rule"]} · {result["severity"]}</div>'
        f'<div class="finding-detail">{result["finding"]}</div>'
        f'<div class="finding-detail"><small>Evidence: {result["evidence"]}</small></div></div>'
    )


def gemini_error_message(error: Exception) -> str:
    error_text = str(error).lower()
    if any(token in error_text for token in ("429", "resource_exhausted", "quota", "rate limit", "rate_limit")):
        return "AI diagnosis is temporarily unavailable because the Gemini API quota has been reached. Deterministic findings remain available."
    return "AI diagnosis is temporarily unavailable. Deterministic findings remain available."


def render_page_header(title: str, description: str = "") -> None:
    """Render a page header with consistent styling."""
    st.markdown(f'<div class="page-header"><div class="page-title">{title}</div>', unsafe_allow_html=True)
    if description:
        st.markdown(f'<p class="page-description">{description}</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


def render_workflow_steps() -> None:
    steps = ["01 CASE", "02 CONTEXT", "03 EVIDENCE", "04 CHECKS", "05 AI ADVISORY", "06 REVIEW"]
    step_html = "".join(
        [f'<span class="workflow-step">{step}</span>'] + [
            '<span class="workflow-arrow">→</span>'
        ] * (len(steps) - 1)
    )
    step_html = step_html.replace('</span><span class="workflow-arrow">→</span><span class="workflow-step">', '</span><span class="workflow-arrow">→</span><span class="workflow-step">')
    st.markdown(f'<div class="workflow-strip">{step_html}</div>', unsafe_allow_html=True)


def render_project_overview_sidebar() -> None:
    total = len(cases)
    evidence_statuses = cases["evidence_status"].fillna("PENDING").value_counts().reindex(["VERIFIED", "REFERENCE", "PENDING"], fill_value=0)
    verified = int(evidence_statuses.get("VERIFIED", 0))
    reference = int(evidence_statuses.get("REFERENCE", 0))
    pending = int(evidence_statuses.get("PENDING", 0))
    total_reviews = len(reviews)

    st.markdown('<div class="sidebar-brief"><strong>Project Status</strong></div>', unsafe_allow_html=True)
    st.markdown('<div class="small-metric">Total Cases</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="small-value">{total}</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-brief" style="margin-top: 0.9rem;"><strong>Evidence Coverage</strong></div>', unsafe_allow_html=True)

    for label, count, cls in [("Verified", verified, "segment-verified"), ("Reference", reference, "segment-reference"), ("Pending", pending, "segment-pending")]:
        st.markdown(f'<div style="display:flex; justify-content:space-between; margin-top:0.5rem; color:var(--text-soft); font-size:0.72rem; font-weight:700; letter-spacing:0.08em; text-transform:uppercase;"><span>{label}</span><span>{count}</span></div>', unsafe_allow_html=True)

    st.markdown('<div class="distribution-bar">' + ''.join(
        [
            f'<span class="distribution-segment {"segment-verified" if label == "Verified" else "segment-reference" if label == "Reference" else "segment-pending"}" style="width:{max(8, (count / max(total,1))*100)}%;"></span>'
            for label, count in [("Verified", verified), ("Reference", reference), ("Pending", pending)]
        ]
    ) + '</div>', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-brief" style="margin-top: 0.9rem;"><strong>Review Records</strong></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="small-value">{total_reviews}</div>', unsafe_allow_html=True)
    api_text = "Configured" if os.getenv("GEMINI_API_KEY") else "Not configured"
    st.markdown('<div class="sidebar-brief" style="margin-top: 0.9rem;"><strong>Gemini</strong></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="small-value" style="font-size:1rem;">{api_text}</div>', unsafe_allow_html=True)


st.markdown(
    """
    <div class="brand-shell">
      <div class="brand-row">
        <div>
          <p class="brand-title">NETSAGE AI</p>
          <p class="brand-subtitle">AI-assisted network troubleshooting</p>
        </div>
        <div class="status-pill"><span class="status-dot"></span> Local Diagnostic Console</div>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

if not DATA.exists():
    st.error("data/cases.csv was not found.")
    st.stop()

cases = load_cases(DATA)
evidence = load_evidence(EVIDENCE)
if not evidence.empty:
    cases = cases.merge(evidence, on="case_id", how="left", suffixes=("", "_evidence"))
    cases["evidence_status"] = cases["evidence_status_evidence"].fillna(cases["evidence_status"])
    cases["evidence_text"] = cases["evidence_text"].fillna("")
    cases["evidence_reference"] = cases["evidence_reference"].fillna("")
validation = validate_case_csv(DATA)
if not validation["valid"]:
    st.warning("CSV validation found issues in the case dataset. The app will continue, but some rows may be incomplete.")
    for error in validation["errors"][:5]:
        st.caption(f"⚠️ {error}")

if cases.empty:
    st.error("The case file is empty or could not be loaded.")
    st.stop()

cases = cases.fillna("")
case_columns = ["case_id", "symptom", "topology_note", "show_outputs", "concept", "severity", "osi_layer", "evidence_source", "verified"]
for col in case_columns:
    if col not in cases.columns:
        cases[col] = ""

reviews = load_reviews(REVIEWS)
if reviews.empty:
    reviews = make_demo_reviews(REVIEWS)

if "review_status" not in cases.columns:
    cases["review_status"] = "Pending"

if "ai_response" not in cases.columns:
    cases["ai_response"] = ""

status_counts = cases["evidence_status"].value_counts()
verified_count = int(status_counts.get("VERIFIED", 0))
reference_count = int(status_counts.get("REFERENCE", 0))
pending_count = int(status_counts.get("PENDING", 0))

with st.sidebar:
    render_project_overview_sidebar()

menu = st.tabs(["Diagnose", "Cases", "Review", "Dashboard", "About"])

with menu[0]:
    render_page_header("Diagnose", "Network troubleshooting workspace")

    st.markdown(
        """
        <div class="workspace-panel">
            <div class="panel-kicker">Case-Based Diagnostics</div>
            <div class="workflow-strip">
                <span class="workflow-step">01 CASE</span>
                <span class="workflow-arrow">→</span>
                <span class="workflow-step">02 CONTEXT</span>
                <span class="workflow-arrow">→</span>
                <span class="workflow-step">03 EVIDENCE</span>
                <span class="workflow-arrow">→</span>
                <span class="workflow-step">04 CHECKS</span>
                <span class="workflow-arrow">→</span>
                <span class="workflow-step">05 AI ADVISORY</span>
                <span class="workflow-arrow">→</span>
                <span class="workflow-step">06 REVIEW</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    selected_case_id = st.selectbox("Choose a case to analyze", cases["case_id"].tolist(), index=0, label_visibility="collapsed")
    row = cases.loc[cases["case_id"].astype(str) == str(selected_case_id)].iloc[0].to_dict()

    status_value = str(row.get("evidence_status", evidence_status(row))).upper()
    badge_class = "badge-verified" if status_value == "VERIFIED" else "badge-reference" if status_value == "REFERENCE" else "badge-pending"

    st.markdown(
        f"""
        <div class="workspace-panel">
            <div class="panel-kicker">Select Troubleshooting Case</div>
            <div class="case-selector">
                <div class="selector-label">Active Case</div>
                <div class="selector-id">{selected_case_id}</div>
                <div class="selector-symptom">{row.get('symptom', '')}</div>
            </div>
            <div class="case-meta-grid">
                <div class="meta-chip"><span class="kicker">Concept</span><span class="value">{row.get('concept', '')}</span></div>
                <div class="meta-chip"><span class="kicker">OSI Layer</span><span class="value">{row.get('osi_layer', '')}</span></div>
                <div class="meta-chip"><span class="kicker">Severity</span><span class="value">{row.get('severity', '')}</span></div>
                <div class="meta-chip"><span class="kicker">Evidence</span><span class="value"><span class="badge {badge_class}">{status_value}</span></span></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### Case Context")
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown(
            f"""
            <div class="workspace-panel">
                <div class="panel-kicker">Symptom</div>
                <div class="detail-value">{row.get('symptom', '')}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            f"""
            <div class="workspace-panel">
                <div class="panel-kicker">Topology</div>
                <div class="detail-value">{row.get('topology_note', '')}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col_b:
        st.markdown(
            f"""
            <div class="workspace-panel">
                <div class="panel-kicker">Classification</div>
                <div class="detail-label">Concept</div><div class="detail-value">{row.get('concept', '')}</div>
                <div class="detail-label" style="margin-top:1rem;">OSI Layer</div><div class="detail-value">{row.get('osi_layer', '')}</div>
                <div class="detail-label" style="margin-top:1rem;">Severity</div><div class="detail-value">{row.get('severity', '')}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("### Evidence & Provenance")
    evidence_text = str(row.get("show_outputs", ""))
    source_name = str(row.get("source_name", "")).strip()
    source_url = str(row.get("source_url", "")).strip()
    source_type = str(row.get("source_type", "")).strip()
    evidence_reference = str(row.get("evidence_reference", "")).strip()
    local_file = str(row.get("local_file", "")).strip()
    evidence_display = str(row.get("evidence_text", "")).strip() or evidence_text

    provenance_lines = []
    if source_name: provenance_lines.append(f"<div class='detail-label'>Source</div><div class='detail-value'>{source_name}</div>")
    if source_type: provenance_lines.append(f"<div class='detail-label'>Source Type</div><div class='detail-value'>{source_type}</div>")
    if evidence_reference: provenance_lines.append(f"<div class='detail-label'>Evidence Reference</div><div class='detail-value'>{evidence_reference}</div>")
    if source_url: provenance_lines.append(f"<div class='detail-label'>Open Source Reference</div><div class='detail-value'><a href='{source_url}' target='_blank'>Open Reference</a></div>")
    if local_file: provenance_lines.append(f"<div class='detail-label'>Local Artifact</div><div class='detail-value'>{local_file}</div>")

    st.markdown(
        f"""
        <div class="workspace-panel">
            <div class="panel-kicker">Evidence Status</div>
            <div class="badge {badge_class}" style="margin-bottom:1rem;">{status_value}</div>
            <div class="detail-value" style="margin-bottom:0.7rem;">{('Public fault/correction evidence documented' if status_value == 'VERIFIED' else 'External reference material; verification required' if status_value == 'REFERENCE' else 'No adequate evidence currently attached')}</div>
            {''.join(provenance_lines)}
            {f"<div class='detail-label' style='margin-top:1rem;'>Evidence Output</div><div class='detail-value'>{evidence_display[:500]}</div>" if evidence_display.strip() else ""}
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### Deterministic Findings")
    st.caption("Rule-based diagnostic baseline")

    analysis_row = dict(row)
    analysis_row["show_outputs"] = str(row.get("evidence_text", "")).strip() or evidence_text
    findings = run_checks(analysis_row)

    if findings:
        for result in findings:
            status = str(result["status"]).lower()
            badge = "pass" if status == "pass" else "warn" if status == "warn" else "fail"
            st.markdown(
                f"""
                <div class="workspace-panel" style="padding:1rem; border-left:4px solid {'var(--success)' if badge == 'pass' else 'var(--warning)' if badge == 'warn' else 'var(--danger)'};">
                    <div class="panel-kicker">{result['rule']}</div>
                    <div class="detail-value" style="margin-bottom:0.5rem;">{result['finding']}</div>
                    <div class="badge {'badge-verified' if badge == 'pass' else 'badge-pending' if badge == 'warn' else 'badge-danger'}">{badge}</div>
                    <div class="detail-label" style="margin-top:1rem;">Evidence</div>
                    <div class="detail-value">{result['evidence']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
    else:
        st.info("No deterministic findings detected for this case.")

    st.divider()
    st.markdown("### Optional AI Advisory")
    st.caption("Advisory — not authoritative")

    if st.button("🤖 Run Diagnosis", type="primary", width="stretch"):
        if not os.getenv("GEMINI_API_KEY"):
            st.warning("AI advisory is unavailable. Deterministic findings remain available.")
        else:
            with st.spinner("Running AI diagnosis..."):
                try:
                    from ai_diagnosis import diagnose_with_gemini
                    result = diagnose_with_gemini(row)
                    st.session_state["last_result"] = result
                    st.session_state["last_case"] = selected_case_id
                except Exception as exc:
                    LOGGER.exception("Gemini diagnosis failed for case %s", selected_case_id)
                    st.error(gemini_error_message(exc))

    if st.session_state.get("last_case") == selected_case_id:
        result = st.session_state.get("last_result", {})
        if result:
            st.markdown(
                """
                <div class="workspace-panel">
                    <div class="panel-kicker">AI Advisory</div>
                    <div class="detail-value">Confidence: {confidence}</div>
                    <div class="detail-value" style="margin-top:0.7rem;">{root_cause}</div>
                </div>
                """.format(
                    confidence=float(result.get("confidence", 0.0)),
                    root_cause=str(result.get("root_cause", "")).strip() or "No root cause identified."
                ),
                unsafe_allow_html=True,
            )
            with st.expander("View AI Details", expanded=True):
                st.json(result)
        else:
            st.info("AI advisory unavailable. Deterministic findings remain available.")

    st.divider()
    st.markdown("### Human Review")
    st.caption("AI recommendations are advisory and require human judgment.")

    decision = st.radio("Your Decision", ["Accepted", "Edited", "Rejected"], horizontal=True, label_visibility="collapsed")
    correction = st.text_area("Notes / Correction Reason", placeholder="Required for Edited or Rejected decisions. Explain your reasoning or correction.", height=80)

    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("💾 Save Review", type="primary", width="stretch"): 
            if decision in ["Edited", "Rejected"] and not correction.strip():
                st.error("Please provide notes or a reason before saving.")
            else:
                payload = st.session_state.get("last_result", {})
                review_record = {
                    "case_id": selected_case_id,
                    "timestamp": pd.Timestamp.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "ai_root_cause": str(payload.get("root_cause", "")).strip(),
                    "ai_confidence": float(payload.get("confidence", 0.0)),
                    "human_decision": decision,
                    "human_root_cause": correction.strip() if decision == "Edited" else str(payload.get("root_cause", "")).strip(),
                    "human_correction": correction.strip(),
                    "reviewer_reason": correction.strip() or "No correction needed.",
                    "evidence_reference": f"{selected_case_id}: {evidence_status(row)} case evidence",
                    "review_source": "real",
                }
                save_review(review_record, REVIEWS)
                st.success(f"✓ Review saved for {selected_case_id}")

with menu[1]:
    render_page_header("Case Library", "Browse and filter the complete collection of 30 troubleshooting cases by concept, OSI layer, severity, or evidence status.")
    
    st.markdown("### Filter Cases")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        concept_filter = st.selectbox("Concept", ["All"] + sorted(cases["concept"].dropna().astype(str).unique().tolist()), label_visibility="collapsed")
    with col2:
        layer_filter = st.selectbox("OSI Layer", ["All"] + sorted(cases["osi_layer"].dropna().astype(str).unique().tolist()), label_visibility="collapsed")
    with col3:
        severity_filter = st.selectbox("Severity", ["All"] + sorted(cases["severity"].dropna().astype(str).unique().tolist()), label_visibility="collapsed")
    with col4:
        evidence_filter = st.selectbox("Evidence Status", ["All", "VERIFIED", "REFERENCE", "PENDING"], label_visibility="collapsed")

    filtered = cases.copy()
    if concept_filter != "All":
        filtered = filtered[filtered["concept"].astype(str).str.lower() == concept_filter.lower()]
    if layer_filter != "All":
        filtered = filtered[filtered["osi_layer"].astype(str).str.lower() == layer_filter.lower()]
    if severity_filter != "All":
        filtered = filtered[filtered["severity"].astype(str).str.lower() == severity_filter.lower()]
    if evidence_filter != "All":
        filtered = filtered[filtered["evidence_status"] == evidence_filter]

    st.markdown(f"**Showing {len(filtered)} of {len(cases)} cases**")
    st.divider()
    
    display_columns = ["case_id", "symptom", "concept", "severity", "evidence_status", "topology_note"]
    st.dataframe(
        filtered[[column for column in display_columns if column in filtered.columns]], 
        width="stretch", 
        hide_index=True,
        column_config={
            "case_id": st.column_config.TextColumn("Case ID", width="small"),
            "symptom": st.column_config.TextColumn("Symptom", width="large"),
            "concept": st.column_config.TextColumn("Concept", width="small"),
            "severity": st.column_config.TextColumn("Severity", width="small"),
            "evidence_status": st.column_config.TextColumn("Evidence", width="small"),
            "topology_note": st.column_config.TextColumn("Topology", width="large"),
        }
    )

with menu[2]:
    render_page_header("Review Audit Log", "Human decisions on AI recommendations. Each record documents a reviewer's evaluation of the AI advisory.")
    
    if reviews.empty:
        st.info("ℹ️ No review records available yet. Start by diagnosing a case on the Diagnose page.")
    else:
        review_display = reviews.copy()
        review_display["review_source"] = review_display["review_source"].fillna("real")
        
        st.info("📋 DEMO/HUMAN REVIEW EXAMPLES — These records demonstrate the workflow. Real reviews would reflect independent human evaluations.")
        
        st.divider()
        st.markdown(f"**Review Summary:** {len(reviews)} records")
        
        col1, col2, col3, col4 = st.columns(4)
        accepted_count = int((review_display["human_decision"].str.lower() == "accepted").sum())
        edited_count = int((review_display["human_decision"].str.lower() == "edited").sum())
        rejected_count = int((review_display["human_decision"].str.lower() == "rejected").sum())
        with col1:
            st.metric("Accepted", accepted_count)
        with col2:
            st.metric("Edited", edited_count)
        with col3:
            st.metric("Rejected", rejected_count)
        with col4:
            total = accepted_count + edited_count + rejected_count
            agreement = (accepted_count / total * 100) if total > 0 else 0
            st.metric("AI-Human Agreement", f"{agreement:.0f}%")
        
        st.divider()
        st.dataframe(
            review_display, 
            width="stretch", 
            hide_index=True,
            column_config={
                "case_id": st.column_config.TextColumn("Case", width="small"),
                "human_decision": st.column_config.TextColumn("Decision", width="small"),
                "ai_root_cause": st.column_config.TextColumn("AI Root Cause", width="medium"),
                "ai_confidence": st.column_config.NumberColumn("Confidence", width="small"),
                "human_root_cause": st.column_config.TextColumn("Human Diagnosis", width="medium"),
                "reviewer_reason": st.column_config.TextColumn("Reason", width="large"),
            }
        )

        if st.button("🔄 Refresh Demo Review Entries", width="content"): 
            make_demo_reviews(REVIEWS)
            reviews = load_reviews(REVIEWS)
            st.success("✓ Demo review entries refreshed.")
            st.rerun()

with menu[3]:
    render_page_header("Dashboard", "Overview of case coverage, evidence status, and human review activity.")
    
    total_cases = len(cases)
    case_status_counts = cases["evidence_status"].value_counts()
    verified_cases = int(case_status_counts.get("VERIFIED", 0))
    reference_cases = int(case_status_counts.get("REFERENCE", 0))
    pending_cases = int(case_status_counts.get("PENDING", 0))
    accepted = int(reviews["human_decision"].fillna("").str.lower().eq("accepted").sum()) if not reviews.empty else 0
    edited = int(reviews["human_decision"].fillna("").str.lower().eq("edited").sum()) if not reviews.empty else 0
    rejected = int(reviews["human_decision"].fillna("").str.lower().eq("rejected").sum()) if not reviews.empty else 0

    st.markdown("### Case Coverage")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Cases", total_cases)
    col2.metric("Verified", verified_cases)
    col3.metric("Reference", reference_cases)
    col4.metric("Pending", pending_cases)

    st.divider()
    st.markdown("### Review Activity")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Accepted", accepted)
    col2.metric("Edited", edited)
    col3.metric("Rejected", rejected)
    review_total = accepted + edited + rejected
    agreement = accepted / review_total if review_total else 0.0
    col4.metric("AI-Human Agreement", f"{agreement:.0%}" if review_total else "No reviews")

    st.divider()
    st.markdown("### Visualizations")
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.markdown("**Evidence Status Distribution**")
        if not cases.empty:
            evidence_dist = cases["evidence_status"].value_counts().sort_index()
            st.bar_chart(evidence_dist)
        else:
            st.info("No case data available.")

    with col_b:
        st.markdown("**Review Decisions**")
        if not reviews.empty:
            decision_dist = reviews["human_decision"].value_counts()
            st.bar_chart(decision_dist)
        else:
            st.info("No review data available.")

    st.divider()
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.markdown("**Cases by Concept**")
        if not cases.empty:
            concept_dist = cases["concept"].value_counts()
            st.bar_chart(concept_dist)
        else:
            st.info("No data available.")

    with col_b:
        st.markdown("**Cases by Severity**")
        if not cases.empty:
            severity_dist = cases["severity"].value_counts()
            st.bar_chart(severity_dist)
        else:
            st.info("No data available.")
    
    st.divider()
    st.markdown("**Cases by OSI Layer**")
    if not cases.empty:
        osi_dist = cases["osi_layer"].value_counts()
        st.bar_chart(osi_dist)
    else:
        st.info("No data available.")

with menu[4]:
    st.header("About NetSage AI")
    st.markdown("AI-Assisted Network Troubleshooting with Deterministic Checks and Human Review")
    st.divider()
    
    st.markdown("### 📌 Overview")
    st.markdown(
        """
        NetSage AI is an educational troubleshooting assistant for Cisco CCNA and Packet Tracer environments. 
        It demonstrates how AI can assist network diagnostics while maintaining human oversight and evidence integrity.
        """
    )
    
    st.markdown("### 🎯 Key Capabilities")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**30 Structured Cases** covering 8 networking domains:")
        st.markdown("""
        - VLAN & Inter-VLAN Routing
        - Gateway / IP Addressing
        - DHCP & DHCP Relay
        - DNS & Name Resolution
        - Static & Dynamic Routing
        - Physical & Logical Interfaces
        - Access Control Lists (ACLs)
        - NAT/PAT & Wireless
        """)
    with col2:
        st.markdown("**Diagnostic Workflow:**")
        st.markdown("""
        1. **Case Selection** — Choose a scenario
        2. **Evidence Review** — Examine provenance
        3. **Deterministic Checks** — Rule-based analysis
        4. **Optional AI Advisory** — Gemini reasoning
        5. **Human Review** — Accept/Edit/Reject
        6. **Audit Trail** — Immutable CSV log
        """)
    
    st.divider()
    st.markdown("### 🛠️ Technology Stack")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("- **Python 3.10+**")
        st.markdown("- **Streamlit** — Web UI")
        st.markdown("- **Pandas** — Data handling")
        st.markdown("- **Google Gemini 2.5** — AI reasoning")
    with col2:
        st.markdown("- **CSV-based** case management")
        st.markdown("- **Deterministic** rule engine")
        st.markdown("- **Offline-capable** UI")
        st.markdown("- **Review logging** & audit trail")
    
    st.divider()
    st.markdown("### 🤝 Responsible AI")
    st.markdown("""
    **Evidence-Grounded Approach:**
    - All AI reasoning is constrained by available evidence
    - Deterministic checks provide a transparent baseline
    - Evidence status remains visible at all times
    - Human review is mandatory before any diagnosis is finalized
    - No fabricated or synthetic claims are permitted
    """)
    
    st.markdown("**Evidence Classification:**")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(status_card("VERIFIED", "Direct public evidence"), unsafe_allow_html=True)
        st.caption("Fault/correction evidence has been documented and inspected.")
    with col2:
        st.markdown(status_card("REFERENCE", "External reference"), unsafe_allow_html=True)
        st.caption("Legitimate lab supports scenario; reproduction may be required.")
    with col3:
        st.markdown(status_card("PENDING", "Needs evidence"), unsafe_allow_html=True)
        st.caption("Adequate evidence was not found.")
    
    st.divider()
    st.markdown("### 📚 Project Structure")
    st.markdown("""
    - **app.py** — Main Streamlit application
    - **src/case_loader.py** — Case & evidence loading
    - **src/rule_checker.py** — Deterministic rule engine (10 rules)
    - **src/ai_diagnosis.py** — Gemini integration
    - **src/review_manager.py** — Review logging & storage
    - **src/validators.py** — CSV validation
    - **data/** — CSV-based case library & evidence manifest
    - **evidence/** — Public lab artifacts & documentation
    """)
    
    st.divider()
    st.markdown("### ⚠️ Limitations")
    st.markdown("""
    - **AI is advisory**, not authoritative
    - Evidence coverage is limited (30 cases)
    - Real network diagnosis requires hands-on troubleshooting
    - Packet Tracer simulations differ from production networks
    - Gemini availability depends on API quota
    - This is an educational tool, not a production system
    """)
    
    st.divider()
    st.markdown("### 📖 Documentation")
    st.markdown("""
    - [Architecture](docs/architecture.md) — System design & data flow
    - [Case Provenance](docs/case_provenance.md) — How evidence was collected
    - [Testing](docs/testing.md) — Test suite and validation
    - [README](README.md) — Installation & usage guide
    """)

review_validation = validate_review_csv(REVIEWS)
if not review_validation["valid"]:
    st.sidebar.warning("Review log validation: some records are malformed.")
evidence_validation = validate_evidence_csv(EVIDENCE)
if not evidence_validation["valid"]:
    st.sidebar.warning("Evidence manifest validation: some records are malformed.")

