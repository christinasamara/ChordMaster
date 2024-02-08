import matplotlib.pyplot as plt
import numpy as np

# Sample deletion time data (replace with your actual data)
deletion_times_chord_16 = [0.002, 0.0025, 0.0022, 0.0028]
deletion_times_chord_32 = [0.003, 0.0032, 0.0029, 0.0035]
deletion_times_chord_64 = [0.004, 0.0042, 0.0038, 0.0045]
deletion_times_chord_128 = [0.005, 0.0052, 0.0048, 0.0055]

# Calculate mean deletion times
mean_deletion_16 = np.mean(deletion_times_chord_16)
mean_deletion_32 = np.mean(deletion_times_chord_32)
mean_deletion_64 = np.mean(deletion_times_chord_64)
mean_deletion_128 = np.mean(deletion_times_chord_128)

# Calculate standard deviations
std_dev_deletion_16 = np.std(deletion_times_chord_16)
std_dev_deletion_32 = np.std(deletion_times_chord_32)
std_dev_deletion_64 = np.std(deletion_times_chord_64)
std_dev_deletion_128 = np.std(deletion_times_chord_128)

# Chord sizes
chord_sizes = [16, 32, 64, 128]
bar_width = 0.2
bar_positions = np.arange(len(chord_sizes))
# Bar plot for mean deletion times
plt.bar(chord_sizes, [mean_deletion_16, mean_deletion_32, mean_deletion_64, mean_deletion_128], color='#33539E', label='Mean Deletion Time')

# Error bars to represent standard deviations
plt.errorbar(chord_sizes, [mean_deletion_16, mean_deletion_32, mean_deletion_64, mean_deletion_128],
             yerr=[std_dev_deletion_16, std_dev_deletion_32, std_dev_deletion_64, std_dev_deletion_128],
             fmt='o', color='#A5678E', label='Standard Deviation')

plt.xlabel('Chord Size')
plt.ylabel('Deletion Time (s)')
plt.xticks(chord_sizes) 
plt.title('Comparison of Deletion Times for Different Chord Sizes')
plt.legend()
plt.show()