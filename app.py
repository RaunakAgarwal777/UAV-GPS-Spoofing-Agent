import pandas as pd
import streamlit as st
from agent import SpoofingAnalysisAgent
from data_loader import generate_sample_data

st.set_page_config(page_title="SentryLink Prototype", layout="wide")
st.title("SentryLink — GPS Spoofing Detection Agent")
st.caption("Modular AI-agent prototype: detect -> explain. One attack, one drone.")

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

    if st.button("Run Analysis Agent"):
        results = [agent.analyze(row) for _, row in df.iterrows()]
        out = pd.concat([df, pd.DataFrame(results)], axis=1)

        st.subheader("Results")
        st.metric("Spoofing alerts", int(out["is_spoofed"].sum()))

        for i, r in out.iterrows():
            if r["is_spoofed"]:
                st.error(f"Row {i}: {r['explanation']}")

        st.dataframe(out, use_container_width=True)
