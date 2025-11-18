import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the dataset (replace with the correct path)
df = pd.read_csv('results.csv')

# Filter for only the 1D and 2D algorithms
df_filtered = df[df['algorithm'].isin(['1D', '2D'])]

# Sort the data by epsilon (ascending order)
df_sorted = df_filtered.sort_values(by='eps')

# Define colors (Orange for 1D, Blue for 2D)
colors = {'1D': 'orange', '2D': 'blue'}

# Plotting
plt.figure(figsize=(10, 6))

# Plotting Actor IMM 1D and Actor IMM 2D
for algorithm in ['1D', '2D']:
    subset = df_sorted[df_sorted['algorithm'] == algorithm]
    
    # Plot the sorted points and connect them with a line
    plt.plot(
        subset['eps'], 
        subset['total time'], 
        marker='o', 
        label=f'Actor IMM {algorithm}', 
        linestyle='-', 
        color=colors[algorithm]
    )

# Set plot labels and title
plt.title('com-DBLP', fontsize=26)
plt.xlabel('epsilon', fontsize=24)
plt.ylabel('Time (s)', fontsize=24)

# Use log scale for the y-axis
plt.yscale('log')

# Set y-axis limits if needed (optional)
# plt.ylim(min_value, max_value)

# Adjust y-axis ticks to show powers of 2 (2, 4, 8, 16, etc.)
y_ticks_values = [2**i for i in range(int(np.floor(np.log2(df_sorted['total time'].min()))), int(np.ceil(np.log2(df_sorted['total time'].max())))+1)]
plt.yticks(y_ticks_values, [str(int(v)) for v in y_ticks_values], fontsize=18)

# Add legend
plt.legend(fontsize=18)

# Adjust the font size for the ticks
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)

# Add grid and show the plot
plt.grid(True, which="both", ls="--", linewidth=0.5)
plt.tight_layout()
plt.savefig('fig10_dblp.png')  # Save the plot
plt.show()  # Show the plot
