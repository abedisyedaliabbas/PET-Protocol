"""
Syed Ali Abbas Abedi

"""
import os
import glob
import pandas as pd
import re

def natural_key(filename):
    # Extract the number after first underscore, before next underscore
    # For example: 03FLIMBD_10_DMSO_... => 10 as int
    match = re.search(r'_(\d+)_', filename)
    if match:
        return int(match.group(1))
    else:
        # If no number found, return a big number so it comes last
        return 1_000_000

energy_last_list = []
name_list = []

files = glob.glob('*.log')

# Sort files naturally by the number after first underscore
files_sorted = sorted(files, key=natural_key)

for filename in files_sorted:
    with open(filename) as f:
        lines = f.readlines()

    energy_all = []
    for line in lines:
        if 'Total Energy, E(TD-HF/TD-DFT)' in line:
            words = line.split()
            if len(words) >= 5:
                energy_all.append(words[4])

    if energy_all:
        name_list.append(filename[:-4])
        energy_last_list.append(energy_all[-1])
    else:
        pass

data = {'Filename': name_list, 'Energy': energy_last_list}
df = pd.DataFrame(data=data)
df.to_csv('data.csv', index=False)
