import numpy as np
import matplotlib.pyplot as plt

def logistic_map(x, a):
    return a * x * (1 - x)

def zero_one_test(a_values):
    initial_condition = 0.5
    num_iterations = 1000
    threshold = 0.01
    
    zero_one_values = []
    for a in a_values:
        x = initial_condition
        
        # Iterate the logistic map
        for _ in range(num_iterations):
            x = logistic_map(x, a)
        
        # Zero-one test
        if np.abs(x - 0.5) > threshold:
            zero_one_values.append(1)  # Chaotic dynamics
        else:
            zero_one_values.append(0)  # Non-chaotic dynamics
    
    # Plotting
    plt.plot(a_values, zero_one_values, '-')
    plt.xlabel("a")
    plt.ylabel("Zero-One Test")
    plt.title("Zero-One Test: Bifurcation in Logistic Map")
    plt.ylim([-0.1, 1.1])
    plt.show()

# Define the range of 'a' values to test
a_values = np.linspace(2, 4, 10000)

# Perform zero-one test and plot the results
zero_one_test(a_values)
