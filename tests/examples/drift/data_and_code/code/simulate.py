"""Wright-Fisher simulations of fixation time under drift (Figure 1, Table 1)."""
import numpy as np
import pandas as pd

N_REPS = 400
POP_SIZES = [50, 100, 200, 400]

rng = np.random.default_rng(11)
rows = []
for N in POP_SIZES:
    for rep in range(N_REPS):
        p, t = 0.5, 0
        while 0 < p < 1:
            p = rng.binomial(2 * N, p) / (2 * N)
            t += 1
        rows.append({"N": N, "rep": rep, "t_fix": t})
sims = pd.DataFrame(rows)

# Table 1: mean time to loss or fixation
table1 = sims.groupby("N")["t_fix"].agg(["mean", "std"]).round(1)
print(table1)
