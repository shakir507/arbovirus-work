import numpy as np
import matplotlib.pyplot as plt

def henon_map(x, y, a):
    new_x = 1 - a * x**2 + y
    new_y = 0.3 * x
    return new_x, new_y

def zero_one_test(a_values):
    initial_conditions = [0.1, 0.1]
    num_iterations = 1000
    threshold = 0.01
    
    zero_one_values = []
    for a in a_values:
        x = initial_conditions[0]
        y = initial_conditions[1]
        
        # Iterate the Hénon map
        for _ in range(num_iterations):
            x, y = henon_map(x, y, a)
        
        # Zero-one test
        if np.abs(x) > threshold:
            zero_one_values.append(1)  # Chaotic dynamics
        else:
            zero_one_values.append(0)  # Non-chaotic dynamics
    
    # Plotting
    plt.plot(a_values, zero_one_values, 'bo')
    plt.xlabel("a")
    plt.ylabel("Zero-One Test")
    plt.title("Zero-One Test: Bifurcation in Hénon Map")
    plt.ylim([-0.1, 1.1])
    plt.show()

# Define the range of 'a' values to test
a_values = np.linspace(0, 1, 200)

# Perform zero-one test and plot the results
zero_one_test(a_values)
