import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv("matrix_kloops_times.csv")

# Group by cores and compute means
grouped = df.groupby('cores').agg(
    mean_matrixGen_time=('matrixGen_time', 'mean'),
    mean_kloops_time=('kloops_time', 'mean')
).reset_index()

# Create equal spacing on x-axis
grouped['x_position'] = np.arange(1, len(grouped) + 1)

plt.figure(figsize=(9, 6))

# Stacked bars
plt.bar(grouped['x_position'], grouped['mean_matrixGen_time'],
        label='Matrix Gen', color='black', width=0.75)

plt.bar(grouped['x_position'], grouped['mean_kloops_time'],
        bottom=grouped['mean_matrixGen_time'],
        label='k Loops', color='orange', width=0.75)

# Axis labels
plt.xlabel("Cores", fontsize=24)
plt.ylabel("Time (sec)", fontsize=24)
plt.title("com-DBLP", fontsize=26)

# Log scale on y-axis
plt.yscale("log")

# ---- Major ticks only (powers of 2) ----
total_times = grouped['mean_matrixGen_time'] + grouped['mean_kloops_time']
y_min = total_times.min()
y_max = total_times.max()

min_exp = int(np.floor(np.log2(y_min)))
max_exp = int(np.ceil(np.log2(y_max)))

y_ticks = [2**e for e in range(min_exp, max_exp + 1)]
plt.yticks(y_ticks, [str(t) for t in y_ticks])

# ---- Major gridlines only ----
plt.grid(True, which='major', linestyle='--', linewidth=0.8)
plt.grid(False, which='minor')   # turn off minor grid completely

# X-ticks with actual core counts
plt.xticks(grouped['x_position'], grouped['cores'].astype(str))

plt.tick_params(axis='both', labelsize=20)

plt.legend()
plt.tight_layout()
plt.savefig("fig13_dblp.png")
plt.show()

