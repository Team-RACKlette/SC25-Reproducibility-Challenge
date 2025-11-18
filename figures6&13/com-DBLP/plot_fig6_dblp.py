import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as st

# Load the results.csv file
df = pd.read_csv("results.csv")

# Filter for only the '1D' and '2D' algorithms
df_filtered = df[df['algorithm'].isin(['1D', '2D'])]

# Group by cores and algorithm, and calculate the mean and standard deviation (for confidence intervals)
grouped = df_filtered.groupby(['cores', 'algorithm']).agg(
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
    ci = st.t.interval(0.95, df=count - 1, loc=mean, scale=std / np.sqrt(count))
    return ci[0], ci[1]

# Apply the function to calculate the CIs for each group
grouped[['ci_lower', 'ci_upper']] = grouped.apply(calculate_ci, axis=1, result_type='expand')

# Filter out rows where the CI values are NaN (if any)
grouped = grouped.dropna(subset=['ci_lower', 'ci_upper'])

# Plotting
plt.figure(figsize=(8, 6))

# Define colors (Orange for 1D, Blue for 2D)
colors = {'1D': 'orange', '2D': 'blue'}

# Plotting Actor IMM 1D and Actor IMM 2D
for algorithm in ['1D', '2D']:
    subset = grouped[grouped['algorithm'] == algorithm]
    
    # Calculate the error relative to the mean for error bars
    # yerr is passed as [lower_errors, upper_errors]
    y_error_lower = subset['mean_time'] - subset['ci_lower']
    y_error_upper = subset['ci_upper'] - subset['mean_time']
    y_error = [y_error_lower.values, y_error_upper.values]
    
    # Plot the mean time using errorbar
    plt.errorbar(
        subset['cores'], 
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
plt.xlabel('Cores', fontsize=24)
plt.ylabel('Time (s)', fontsize=24)

# Use log scale for both axes, with base 2 for the y-axis
plt.xscale('log', base=2)
plt.yscale('log', base=2)

# Adjust X-ticks to show actual core counts
unique_cores = sorted(grouped['cores'].unique())
plt.xticks(unique_cores, [str(c) for c in unique_cores])

# Determine appropriate powers of 2 for y-axis ticks
min_val = grouped['ci_lower'].min()
max_val = grouped['ci_upper'].max()

# Robust handling for NaN or non-positive min/max values on log scale
if np.isnan(min_val) or min_val <= 0:
    min_val = 0.1
if np.isnan(max_val) or max_val <= 0:
    max_val = 1000

min_power = int(np.floor(np.log2(min_val)))
max_power = int(np.ceil(np.log2(max_val)))
y_ticks_values = [2**i for i in range(min_power, max_power + 1)]

# Format the labels: integer if >= 1, format as float (e.g., 0.50, 0.25) if < 1
y_tick_labels = [str(int(v)) if v >= 1 else f'{v:.2f}' for v in y_ticks_values]
plt.yticks(y_ticks_values, y_tick_labels)


plt.minorticks_off() # Turn off minor ticks to avoid clutter

# Add grid and legend
plt.grid(True, which="major", ls="--", linewidth=0.5)
plt.legend()

# Save the figure
plt.savefig('fig6_dblp.png')
plt.close()