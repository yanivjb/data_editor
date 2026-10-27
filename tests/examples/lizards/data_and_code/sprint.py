import os
import pandas as pd
os.chdir("/Users/jdoe/Dropbox/lizards")
d = pd.read_excel("Lizard data FINAL v3.xlsx", sheet_name="field data")
d = d[d["Sprint speed (m/s)"] != "escaped"]
d["speed"] = d["Sprint speed (m/s)"].astype(float)
import numpy as np
obs = d.groupby("Habitat")["speed"].mean()
diff = obs["rock"] - obs["sand"]
perm = []
for i in range(10000):
    lab = np.random.permutation(d["Habitat"].values)
    m = d.assign(h=lab).groupby("h")["speed"].mean()
    perm.append(m["rock"] - m["sand"])
p = np.mean(np.abs(perm) >= abs(diff))
print(obs, diff, p)
