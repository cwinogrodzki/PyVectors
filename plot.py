import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Data dictionary
data = {
    'Hardware': ['Intel-Skylake'] * 3 + ['AMD-EPYC-milan'] * 3 + ['AMD-mi250'] + ['Arm-Ampere'] * 3 + ['Nvidia-A100'] + ['Apple M2 Max'] * 3 + ['Apple M2 Max- MPS'],
    'Kernel': ['3d stencil'] * 15,
    'Framework': ['Numpy', 'Pytorch', 'Naïve', 'Numpy', 'Pytorch', 'Naïve',
                  'Pytorch', 'Numpy', 'Pytorch', 'Naïve', 'Pytorch', 'Numpy', 'Pytorch', 'Naïve', 'Pytorch'],
    'Time (ms)': [167.4469, 0.2716, 9795.1974, 67.8771, 0.293, 7792.7929,
                  0.0353, 137.1123, 1.6921, 13944.7625, 0.0766, 5.9222, 15.9677, 421.1531, 7.3955]
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Pivot table to prepare for grouped bar plot
pivot_df = df.pivot_table(index='Hardware', columns='Framework', values='Time (ms)')

# Drop columns with NaN values (if there are any hardware-framework combinations with no data)
pivot_df = pivot_df.dropna(axis=1, how='all')
pivot_df = pivot_df.dropna(axis=0, how='all')

# Plot settings
fig, ax = plt.subplots(figsize=(12, 7))
bar_width = 0.15  # Width of each bar
x = np.arange(len(pivot_df))  # x positions for frameworks

# Plot each hardware as a separate set of bars
for i, framework in enumerate(pivot_df.columns):
    ax.bar(x + i * bar_width, pivot_df[framework], width=bar_width, label=framework)

# Customize the plot
ax.set_title('3d Stenciil Performance')
ax.set_xlabel('Framework')
ax.set_ylabel('Time (ms)')
ax.set_yscale('log')  # Use logarithmic scale for better visualization
ax.set_xticks(x + bar_width * (len(pivot_df.columns) - 1) / 2)  # Center xticks
ax.set_xticklabels(pivot_df.index)  # Framework labels
ax.legend(title='Hardware')
plt.xticks(rotation=45)

# Layout adjustments and plot display
plt.tight_layout()
plt.show()