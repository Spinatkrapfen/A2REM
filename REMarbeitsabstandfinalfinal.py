# -*- coding: utf-8 -*-
"""
Created on Sun Nov 26 11:56:41 2023

@author: theo
"""

import numpy as np
from scipy.signal import find_peaks
import matplotlib.pyplot as plt

def calculate_snr(file_paths):
    snr_values = []
    for file_info in file_paths:
        data = np.loadtxt(file_info['file_path'])
        y_values = data[:, 1]

        first_300 = y_values[80:320]
        data_mean = np.mean(first_300)
        data_std = np.std(first_300)           

        # Find peaks for BSE sensor (lowest valleys)
        if 'BSE' in file_info['file_path']:
            peaks, _ = find_peaks(-y_values, distance=100)
            lowest_valley_indices = np.argsort(y_values[peaks])[:2]
            lowest_valley_indices = peaks[lowest_valley_indices]
            signal_peaks = y_values[lowest_valley_indices]
            
        # Find peaks for InLens and SE sensors (highest peaks)
        else:
            peaks, _ = find_peaks(y_values, distance=100)
            highest_peak_indices = np.argsort(y_values[peaks])[-2:][::-1]
            highest_peak_indices = peaks[highest_peak_indices]
            signal_peaks = y_values[highest_peak_indices]

            
        signal_mean = np.mean(signal_peaks)
        signal_true = np.abs(signal_mean - data_mean)
        snr = signal_true / data_std

        snr_values.append(snr)

    return snr_values

file_paths_BSE = [
    {'file_path': r'BSE26', 'distance': 26.5},
    {'file_path': 'BSE21', 'distance': 21.3},
    {'file_path': 'BSE16', 'distance': 16.2},
    {'file_path': 'BSE11', 'distance': 11.2},
    {'file_path': 'BSE6', 'distance': 6.4},
]

file_paths_InLens = [
    {'file_path': 'InLens26', 'distance': 26.5},
    {'file_path': 'InLens21', 'distance': 21.3},
    {'file_path': 'InLens16', 'distance': 16.2},
    {'file_path': 'InLens11', 'distance': 11.2},
    {'file_path': 'InLens6', 'distance': 6.4},
]

file_paths_SE = [
    {'file_path': 'SE26', 'distance': 26.5},
    {'file_path': 'SE21', 'distance': 21.3},
    {'file_path': 'SE16', 'distance': 16.2},
    {'file_path': 'SE11', 'distance': 11.2},
    {'file_path': 'SE6', 'distance': 6.4},
]

# Calculate SNR for each sensor type
snr_values_BSE = calculate_snr(file_paths_BSE)
snr_values_InLens = calculate_snr(file_paths_InLens)
snr_values_SE = calculate_snr(file_paths_SE)

# Extract distances from file_info for each sensor type
distances_BSE = [file_info['distance'] for file_info in file_paths_BSE]
distances_InLens = [file_info['distance'] for file_info in file_paths_InLens]
distances_SE = [file_info['distance'] for file_info in file_paths_SE]

# Plot SNR for each sensor type
plt.figure(figsize=(8, 6))
plt.plot(distances_BSE, snr_values_BSE, marker='o', linestyle='-', color='blue', label='BSE')
plt.plot(distances_InLens, snr_values_InLens, marker='o', linestyle='-', color='green', label='InLens')
plt.plot(distances_SE, snr_values_SE, marker='o', linestyle='-', color='red', label='SE')
plt.xlabel('Abstand / mm')
plt.ylabel('SNR')
plt.title('SNR vs Abstand für unterschiedliche Sensoren')
plt.legend()
plt.grid(True)
plt.show()
