import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy import fft

def henon_map(x, y, z, a, b, c, d):
    new_x = y + 1 - a * x**2 + z
    new_y = b * x
    new_z = c - d * x**2
    return new_x, new_y, new_z

def hyperchaotic_henon_map(x, y, z, a, b, c, d, num_iterations):
    x_values = []
    y_values = []
    z_values = []
    for _ in range(num_iterations):
        x, y, z = henon_map(x, y, z, a, b, c, d)
        x_values.append(x)
        y_values.append(y)
        z_values.append(z)
    return np.array(x_values), np.array(y_values), np.array(z_values)

# Parameters for the Hénon map
a = 1.4
b = 0.3
c = 0.2
d = 1.1

# Parameters for power spectrum analysis
num_iterations = 5000
sampling_rate = 1  # Set to 1 for discrete-time system

# Generate the time series
x_values, y_values, z_values = hyperchaotic_henon_map(0, 0, 0, a, b, c, d, num_iterations)

# Perform power spectrum analysis
x_fft = fft.fft(x_values)
y_fft = fft.fft(y_values)
z_fft = fft.fft(z_values)
freq = fft.fftfreq(len(x_values), d=1/sampling_rate)

# Plotting the power spectrum
plt.figure(figsize=(8, 5))
plt.plot(freq[:len(freq)//2], np.abs(x_fft[:len(freq)//2])**2, label='X')
plt.plot(freq[:len(freq)//2], np.abs(y_fft[:len(freq)//2])**2, label='Y')
plt.plot(freq[:len(freq)//2], np.abs(z_fft[:len(freq)//2])**2, label='Z')
plt.xlabel('Frequency')
plt.ylabel('Power Spectrum')
plt.title('Power Spectrum Analysis of Hyperchaotic Hénon Map (3D)')
plt.legend()
plt.grid(True)
plt.show()
