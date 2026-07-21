"""Explainer: converts a raw flag into a human-readable report.
WHY: operators need to trust WHY a system raised an alert, not just a
score. This is a template-based generator today; swap the return line
for a LangChain LLM call later without changing any other file.
"""
from knowledge_base import retrieve


def explain(row: dict, is_spoofed: bool, confidence: float):
    if not is_spoofed:
        return "No anomaly detected. Telemetry consistent with normal flight."

    query = (f"gps speed {row['gps_speed']:.1f} imu speed "
             f"{row['imu_speed']:.1f} altitude jump {row['alt_jump']:.1f}")
    match = retrieve(query, top_k=1)[0]
    return (f"Spoofing suspected (confidence {confidence:.0%}). "
            f"Matches known pattern {match['id']}: {match['text']}")
