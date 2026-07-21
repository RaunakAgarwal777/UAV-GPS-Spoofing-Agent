# SentryLink V1

**Explainable AI Agent for GPS Spoofing Detection in Autonomous UAV Communication Systems**

A lightweight, modular proof-of-concept demonstrating AI agents, explainable AI (RAG),
and swappable-module architecture for UAV cybersecurity. Not military software —
a research prototype for a single attack (GPS spoofing) on a single UAV.

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Architecture
```
UAV Telemetry → Sensor (parser) → Detector Agent (RandomForest)
                                        ↓ (if flagged)
                              Knowledge Base (TF-IDF signatures)
                                        ↓
                              Explainer Agent → Dashboard
```

## Modules

| File | Role | Type |
|---|---|---|
| `data_loader.py` | Generates/loads sample telemetry | deterministic |
| `detector.py` | RandomForest classifier — flags spoofing | ML |
| `knowledge_base.py` | TF-IDF retrieval over attack signatures (RAG) | retrieval |
| `explainer.py` | Turns detection + retrieved signature into plain-English report | AI agent output |
| `agent.py` | `SpoofingAnalysisAgent` — orchestrates detector + explainer | AI agent |
| `app.py` | Streamlit dashboard | frontend |

Each module is independently swappable — e.g. replace `detector.py`'s model,
or `knowledge_base.py`'s TF-IDF with FAISS embeddings, without touching anything else.

## Roadmap
Prototype (this repo) → real dataset + evaluation metrics → Coordinator agent +
multi-attack support → research paper.

## Deploy
Push to GitHub → connect repo on [Streamlit Community Cloud](https://streamlit.io/cloud) →
point at `app.py` → done.
