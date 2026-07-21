"""SpoofingAnalysisAgent: orchestrates detection + explanation.
This is the ONE agent in today's prototype. Detector and Explainer are
plain modules it calls. Promoting either into its own independent agent
later (e.g. a Coordinator managing several detectors) needs no rewrite
here -- that's the "big architecture, tiny prototype" property.
"""
from detector import SpoofingDetector
from explainer import explain


class SpoofingAnalysisAgent:
    def __init__(self):
        self.detector = SpoofingDetector()

    def analyze(self, row: dict):
        is_spoofed, confidence = self.detector.predict(row)
        explanation = explain(row, is_spoofed, confidence)
        return {
            "is_spoofed": is_spoofed,
            "confidence": confidence,
            "explanation": explanation,
        }
