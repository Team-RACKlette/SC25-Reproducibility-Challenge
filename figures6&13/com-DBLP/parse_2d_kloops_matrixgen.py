#!/usr/bin/env python3
import os
import re
import csv

LOG_DIR = "results"
OUTPUT_CSV = "matrix_kloops_times.csv"

# Regex to extract nodes, cores, repetition from filename
# Example: log_1n_48c_2D_r1.txt
fname_re = re.compile(r"log_(\d+)n_(\d+)c_2D_r(\d+)\.txt$")

# Regex to extract the "Time until now" values
matrix_re = re.compile(r"\[Time until now\] in matrixGen:\s+([0-9.]+)\s+seconds")
kloops_re = re.compile(r"\[Time until now\] in k loops:\s+([0-9.]+)\s+seconds")

rows = []

for fname in os.listdir(LOG_DIR):
    # Only process Actor IMM 2D logs
    if not fname.startswith("log_") or "2D" not in fname or not fname.endswith(".txt"):
        continue

    m = fname_re.match(fname)
    if not m:
        continue

    nodes = int(m.group(1))
    cores = int(m.group(2))
    rep   = int(m.group(3))

    last_matrix = None
    last_kloops = None

    with open(os.path.join(LOG_DIR, fname), "r") as f:
        for line in f:
            mm = matrix_re.search(line)
            if mm:
                last_matrix = float(mm.group(1))
            mk = kloops_re.search(line)
            if mk:
                last_kloops = float(mk.group(1))

    # Only write a row if we found both timings
    if last_matrix is not None and last_kloops is not None:
        rows.append([nodes, cores, rep, last_kloops, last_matrix])

# Write CSV
with open(OUTPUT_CSV, "w", newline="") as out:
    writer = csv.writer(out)
    writer.writerow(["nodes", "cores", "repetition", "kloops_time", "matrixGen_time"])
    writer.writerows(rows)

print(f"Wrote {len(rows)} rows to {OUTPUT_CSV}")

