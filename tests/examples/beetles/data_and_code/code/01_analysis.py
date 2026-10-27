"""Survival of dung beetles under a heat treatment.

Run from data_and_code/:  python code/01_analysis.py
"""
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

beetles = pd.read_csv("data/beetles.csv")

# Table 1: survival by treatment with bootstrap 95% CIs
rng = np.random.default_rng(2024)
rows = []
for trt, d in beetles.groupby("treatment"):
    boots = [rng.choice(d["survived"], len(d)).mean() for _ in range(5000)]
    rows.append({"treatment": trt, "n": len(d), "survival": d["survived"].mean(),
                 "ci_low": np.percentile(boots, 2.5), "ci_high": np.percentile(boots, 97.5),
                 "mass_mg": d["mass_mg"].mean()})
table1 = pd.DataFrame(rows)
table1.round(3).to_csv("outputs/table1.csv", index=False)

# Difference in survival (Results, paragraph 1)
ctrl = beetles.query("treatment == 'control'")["survived"].to_numpy()
heat = beetles.query("treatment == 'heat'")["survived"].to_numpy()
diffs = [rng.choice(ctrl, len(ctrl)).mean() - rng.choice(heat, len(heat)).mean() for _ in range(5000)]
diff = ctrl.mean() - heat.mean()
print(f"difference = {diff:.3f} (95% CI {np.percentile(diffs, 2.5):.3f} to {np.percentile(diffs, 97.5):.3f})")

# Figure 2: survival by treatment
fig, ax = plt.subplots(figsize=(4, 3))
ax.errorbar(table1["treatment"], table1["survival"],
            yerr=[table1["survival"] - table1["ci_low"], table1["ci_high"] - table1["survival"]], fmt="o")
ax.set_ylabel("Proportion surviving")
fig.tight_layout()
fig.savefig("outputs/fig2.png", dpi=200)
