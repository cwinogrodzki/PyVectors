import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# *******3D STENCIL*******
# group by hardware
stencil_hardware = ('Intel', 'AMD-CPU', 'AMD-GPU', 'ARM-CPU', 'Nvidia-GPU', 'Apple-CPU', 'Apple-GPU')
stencil_results = {
    'Numpy': (167.4469, 67.8771, 0, 137.1123, 0, 5.9222, 0),
    'Pytorch': (0.2716, 0.293, 0.0353, 1.6921, 0.0766, 15.9677, 7.3955),
    'Naive': (9795.1974, 7792.7929, 0, 13944.7625, 0, 421.1531, 0)
}

# group by framework
framework = ('Numpy', 'Pytorch', 'Naive')
results_ = {
    'Intel-Skylake': (167.4469, 0.2716, 9795.1974), 
    'AMD-EPYC-milan': (67.8771, 0.293, 7792.7929),
    'AMD-mi250': (0,  0.0353, 0),
    'Arm-Ampere': (137.1123, 1.6921, 13944.7625),
    'Nvidia-A100': (0, 0.0766, 0),
    'Apple M2 Max': (5.9222, 15.9677, 421.1531),
    'Apple M2 Max MPS': (0, 7.3955, 0)
}

# ********GEMM***********
# group by hardware
gemm_hardware = ('Intel', 'AMD-CPU', 'AMD-GPU', 'ARM-CPU', 'Nvidia-GPU', 'Apple-CPU', 'Apple-GPU')
gemm_results = {
    'Numpy': (0.5497, 1.0577, 0, 0.6767, 0, 1.0068, 0),
    'Pytorch': (0.3982, 0, 0.0069, 221.4884, 0.0124, 0.2255, 0.0214),
    'Naive': (66590.0677, 48635.6283, 0, 94091.2423, 0, 36656.0805, 0)
}

# *********ATAX***********
# group by hardware
atax_hardware = ('Intel', 'AMD-CPU', 'AMD-GPU', 'ARM-CPU', 'Nvidia-GPU', 'Apple-CPU', 'Apple-GPU')
atax_results = {
    'Numpy': (0.0151, 0.0129, 0, 0.0083, 0, 0.0125, 0),
    'Pytorch': (0.0056, 0.0407, 0.0033, 0.2715, 0.0042, 0.006, 0.0073),
    'Naive': (92.5321, 65.9915, 0, 0, 0, 56.5335, 0)
}

hardware = stencil_hardware
results = stencil_results

x = np.arange(len(hardware))
#x = np.arange(len(framework))
width = .25
multiplier = 0
colors = ('darkblue', 'royalblue', 'lightsteelblue')

fig, ax = plt.subplots(layout='constrained')

for framework, time in results.items():
    offset = width * multiplier
    color = colors[multiplier % len(colors)]
    rects = ax.bar(x + offset, time, width, color=color, label=framework)
    #ax.bar_label(rects, padding=3)
    multiplier += 1

ax.set_title('3d Stencil Performance', fontsize=15)
ax.set_ylabel('Time (ms)')
ax.set_yscale('log')  # Use logarithmic scale for better visualization
ax.set_xticks(x + width, hardware)  # Center xticks
#ax.set_xticklabels(pivot_df.index)  # Framework labels
ax.legend(loc='upper right', ncols=3)
plt.xticks(rotation=45)

plt.show()