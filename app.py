import pandas as pd
import streamlit as st
from agent import SpoofingAnalysisAgent
from data_loader import generate_sample_data

st.set_page_config(page_title="HappyLink Prototype", layout="wide")
st.title("🟢 HappyLink — GPS Spoofing Detection Agent v.01")
st.caption("Modular AI-agent prototype: detect -> explain. One attack, one drone.")

# ---------- UPGRADE 1: "How this works" explainer for non-technical viewers ----------
with st.expander("ℹ️ How Our Agent works (click to read — 30 seconds)", expanded=True):
    st.markdown("""
    **In plain English:**
    1. A drone constantly reports its speed two ways — once from **GPS** satellites,
       once from its own onboard motion sensors (**IMU**).
    2. Normally these two numbers roughly agree.
    3. Our AI Agent checks every reading — if GPS and IMU strongly disagree,
       it's a sign someone may be faking the GPS signal (**spoofing**).
    4. When flagged, the system looks up the closest matching known attack
       pattern and explains the alert in plain language — not just a raw score.
    """)

# ---------- UPGRADE 2: data dictionary so column names aren't confusing ----------
with st.expander("📖 What do these columns mean?"):
    st.markdown("""
    | Column | Meaning |
    |---|---|
    | `gps_speed` | Speed as reported by GPS satellites |
    | `imu_speed` | Speed as measured by the drone's own motion sensors |
    | `alt_jump` | How much altitude suddenly changed |
    | `is_spoofed` | AI Agent's verdict: attack suspected or not |
    | `confidence` | How sure the AI Agent is (0–100%) |
    | `explanation` | Plain-English reason for the alert |
    """)

agent = SpoofingAnalysisAgent()

source = st.radio("Telemetry source", ["Sample data", "Upload CSV"])
if source == "Upload CSV":
    file = st.file_uploader("CSV with columns: gps_speed, imu_speed, alt_jump")
    df = pd.read_csv(file) if file else None
else:
    df = generate_sample_data()

if df is not None:
    st.subheader("Telemetry stream")
    st.dataframe(df, use_container_width=True)

    if st.button("Run Vulnerability Analysis Agent"):
        results = [agent.analyze(row) for _, row in df.iterrows()]
        out = pd.concat([df, pd.DataFrame(results)], axis=1)

        st.subheader("Results")

        # ---------- UPGRADE 2 (cont.): traffic-light status cards ----------
        n_alerts = int(out["is_spoofed"].sum())
        n_total = len(out)
        col1, col2, col3 = st.columns(3)
        col1.metric("Total readings", n_total)
        col2.metric("Spoofing alerts", n_alerts)
        status = "🔴 Attack detected! " if n_alerts > 0 else "🟢 All clear Mate!"
        col3.metric("System status", status)

        # ---------- UPGRADE 3: simple visual chart, not just a table ----------
        st.subheader("Normal vs. Suspicious readings")
        chart_data = out["is_spoofed"].map({True: "Suspicious", False: "Normal"})
        st.bar_chart(chart_data.value_counts())

        # ---------- UPGRADE 3 (cont.): expandable plain-English reason per row ----------
        st.subheader("Alert details")
        flagged = out[out["is_spoofed"]]
        if flagged.empty:
            st.success("No spoofing detected in this telemetry batch.")
        else:
            for i, r in flagged.iterrows():
                with st.expander(f"⚠️ Row {i} — {r['confidence']:.0%} confidence"):
                    st.write(r["explanation"])
                    st.write(f"GPS speed: {r['gps_speed']:.2f} | "
                              f"IMU speed: {r['imu_speed']:.2f} | "
                              f"Altitude jump: {r['alt_jump']:.2f}")

        st.subheader("Full results table")
        st.dataframe(out, use_container_width=True)
