"""Detector: lightweight ML classifier for GPS spoofing.
WHY: separates the 'is this an attack pattern' decision from explanation
logic, so it can be swapped for a better model later without touching
anything else in the system.
"""
import numpy as np
from sklearn.ensemble import RandomForestClassifier


def _synthetic_training_data(n=200):
    rng = np.random.default_rng(42)
    normal = rng.normal(0, 1, (n, 4))
    normal[:, 2] = np.abs(normal[:, 0] - normal[:, 1])          # small mismatch
    spoofed = rng.normal(0, 1, (n, 4))
    spoofed[:, 2] = np.abs(spoofed[:, 0] - spoofed[:, 1]) + 8   # injected mismatch
    spoofed[:, 3] += 15                                          # sudden alt jump
    X = np.vstack([normal, spoofed])
    y = np.array([0] * n + [1] * n)
    return X, y


class SpoofingDetector:
    def __init__(self):
        X, y = _synthetic_training_data()
        self.model = RandomForestClassifier(n_estimators=50, random_state=42)
        self.model.fit(X, y)

    def predict(self, row: dict):
        mismatch = abs(row["gps_speed"] - row["imu_speed"])
        x = np.array([[row["gps_speed"], row["imu_speed"], mismatch, row["alt_jump"]]])
        proba = self.model.predict_proba(x)[0][1]
        return bool(proba > 0.5), float(proba)
