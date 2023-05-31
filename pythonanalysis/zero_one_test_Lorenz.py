import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

def lorenz_system(t, X, sigma, rho, beta):
    x, y, z = X
    dx_dt = sigma * (y - x)
    dy_dt = x * (rho - z) - y
    dz_dt = x * y - beta * z
    return [dx_dt, dy_dt, dz_dt]

def zero_one_test(sigma_values):
    rho = 28.0
    beta = 8.0 / 3.0
    initial_conditions = [1.0, 0.0, 0.0]
    num_points = 10000
    threshold = 0.01
    
    zero_one_values = []
    for sigma in sigma_values:
        time = np.linspace(0, 100, num_points)
        solution = solve_ivp(lambda t, X: lorenz_system(t, X, sigma, rho, beta),
                             [0, 100], initial_conditions, t_eval=time)
        x_values = solution.y[0]
        
        # Zero-one test
        max_diff = np.max(np.abs(np.diff(x_values)))
        if max_diff > threshold:
            zero_one_values.append(1)  # Chaotic dynamics
        else:
            zero_one_values.append(0)  # Non-chaotic dynamics
    
    # Plotting
    plt.plot(sigma_values, zero_one_values, 'bo')
    plt.xlabel("Sigma")
    plt.ylabel("Zero-One Test")
    plt.title("Zero-One Test: Bifurcation in Lorenz System")
    plt.ylim([-0.1, 1.1])
    plt.show()

# Define the range of sigma values to test
sigma_values = np.linspace(0, 50, 200)

# Perform zero-one test and plot the results
zero_one_test(sigma_values)
