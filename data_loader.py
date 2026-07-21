"""Generates sample telemetry so the demo runs with zero setup / no dataset needed."""
import numpy as np
import pandas as pd


def generate_sample_data(n_normal=15, n_spoofed=5):
    rng = np.random.default_rng(1)
    rows = []
    for _ in range(n_normal):
        s = rng.normal(10, 1)
        rows.append({"gps_speed": s, "imu_speed": s + rng.normal(0, 0.3),
                      "alt_jump": rng.normal(0, 0.5)})
    for _ in range(n_spoofed):
        gps = rng.normal(10, 1)
        rows.append({"gps_speed": gps, "imu_speed": gps - rng.uniform(6, 10),
                      "alt_jump": rng.uniform(10, 20)})
    return pd.DataFrame(rows).sample(frac=1, random_state=2).reset_index(drop=True)
