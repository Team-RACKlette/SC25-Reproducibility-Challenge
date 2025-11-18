import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as st

# Load the results CSV file, now using 'results_parsed_dblp.csv'
df = pd.read_csv("results_parsed.csv")

# Filter for only the '1D' and '2D' algorithms
df_filtered = df[df['algorithm'].isin(['1D', '2D'])]

# UPDATED GROUPING: Group by 'k' and 'algorithm'
grouped = df_filtered.groupby(['k', 'algorithm']).agg(
    mean_time=('total time', 'mean'),
    std_time=('total time', 'std'),
    count=('total time', 'count')
).reset_index()

# Function to calculate the 95% confidence interval for a row
def calculate_ci(row):
    mean = row['mean_time']
    std = row['std_time']
    count = row['count']

    # Cannot calculate CI if count < 2 (degrees of freedom df=count-1)
    if count < 2:
        return np.nan, np.nan

    # Calculate the 95% confidence interval
    # The confidence interval is based on the t-distribution since the population standard deviation is unknown
    ci = st.t.interval(0.95, df=count - 1, loc=mean, scale=std / np.sqrt(count))
    return ci[0], ci[1]

# Apply the function to calculate the CIs for each group
grouped[['ci_lower', 'ci_upper']] = grouped.apply(calculate_ci, axis=1, result_type='expand')

# Filter out rows where the CI values are NaN (if any)
grouped = grouped.dropna(subset=['ci_lower', 'ci_upper'])

# Plotting setup
plt.figure(figsize=(10, 6))

# Define colors (Orange for 1D, Blue for 2D)
colors = {'1D': 'orange', '2D': 'blue'}

# Plotting for 1D and 2D algorithms
for algorithm in ['1D', '2D']:
    subset = grouped[grouped['algorithm'] == algorithm]

    # Calculate the error relative to the mean for error bars
    # yerr is passed as [lower_errors, upper_errors]
    y_error_lower = subset['mean_time'] - subset['ci_lower']
    y_error_upper = subset['ci_upper'] - subset['mean_time']
    y_error = [y_error_lower.values, y_error_upper.values]

    # Plot the mean time using errorbar
    plt.errorbar(
        subset['k'],
        subset['mean_time'],
        yerr=y_error,
        marker='o',
        label=f'Actor IMM {algorithm}',
        linestyle='-',
        color=colors[algorithm],
        capsize=4,       # Size of the error bar caps
        elinewidth=1.5   # Thickness of the error bar lines
    )

# Set plot labels and title
plt.title('com-DBLP', fontsize=26)
plt.xlabel('k', fontsize=24)
plt.ylabel('Time (s)', fontsize=24)

# Use log scale for both axes, with base 2
plt.xscale('log', base=2)
plt.yscale('log', base=2)

# Adjust X-ticks to show actual K values
unique_k_values = sorted(grouped['k'].unique())
# Correctly use plt.xticks() for the current axes
plt.xticks(unique_k_values, [str(k) for k in unique_k_values], fontsize=18) 

# Determine appropriate powers of 2 for y-axis ticks
min_val = grouped['ci_lower'].min()
max_val = grouped['ci_upper'].max()

# Robust handling for NaN or non-positive min/max values on log scale
if np.isnan(min_val) or min_val <= 0:
    min_val = 0.1
if np.isnan(max_val) or max_val <= 0:
    max_val = 1000

min_power = int(np.floor(np.log2(min_val)))
# MODIFICATION START: Ensure max_power is at least 8 (for 2^8 = 256)
target_max_power = 8 # 2^8 = 256
max_power_data = int(np.ceil(np.log2(max_val)))

# Set the maximum power to the larger of the data maximum or 8
max_power = max(max_power_data, target_max_power)

y_ticks_values = [2**i for i in range(min_power, max_power + 1)]
# MODIFICATION END

# Format the labels: integer if >= 1, format as float (e.g., 0.50, 0.25) if < 1
y_tick_labels = [str(int(v)) if v >= 1 else f'{v:.2f}' for v in y_ticks_values]

# Correctly use plt.yticks() for the current axes, passing values, labels, and font size
plt.yticks(y_ticks_values, y_tick_labels, fontsize=18) 


plt.minorticks_off() # Turn off minor ticks to avoid clutter

# Add grid and legend
plt.grid(True, which="major", ls="--", linewidth=0.5)
plt.legend(fontsize=16) # Setting a reasonable legend font size

# Save the figure
plt.savefig('fig8_dblp.png')
plt.close()