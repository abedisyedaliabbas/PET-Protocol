"""
Syed Ali Abbas Abedi

"""

import os, glob, re
import pandas as pd

def natsort_key(s):
    # splits "MOL_10.log" -> ["MOL_", 10, ".log"] for human ordering
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r'(\d+)', s)]

energy_last_list = []
name_list = []

files = sorted(glob.glob('*.log'), key=natsort_key)

for fn in files:
    with open(fn, errors='ignore') as f:
        lines = f.readlines()
    name_list.append(fn[:-4])
    energy_all = []
    for line in lines:
        if 'SCF Done:  E(UM062X) =' in line:
            words = line.split()
            energy_all.append(float(words[4]))
    # if no SCF line found, skip or set None
    energy_last_list.append(energy_all[-1] if energy_all else None)

df = pd.DataFrame({'Filename': name_list, 'Energy': energy_last_list})
df.to_csv('data.csv', index=False)
