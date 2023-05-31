import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from SALib.sample import saltelli
from SALib.analyze import sobol

# Define the SIR model equations
def sir_model(y, t, beta, gamma):
    S, I, R = y
    dSdt = -beta * S * I
    dIdt = beta * S * I - gamma * I
    dRdt = gamma * I
    return [dSdt, dIdt, dRdt]

# Define the parameter ranges for sampling
problem = {
    'num_vars': 2,
    'names': ['beta', 'gamma'],
    'bounds': [[0.1, 0.5], [0.05, 0.2]]
}

# Set up the model evaluation function
def evaluate_model(params):
    # Set initial conditions
    y0 = [0.99, 0.01, 0.0]
    t = np.linspace(0, 100, 100)  # Time grid

    # Solve the SIR model with the given parameters
    solution = odeint(sir_model, y0, t, args=tuple(params))
    return solution[:, 1]  # Return the Infectious (I) compartment

# Generate parameter samples using Saltelli's sampling
param_values = saltelli.sample(problem, 1000)

# Run the model for each parameter sample
model_outputs = np.zeros(param_values.shape[0])
for i, params in enumerate(param_values):
    model_outputs[i] = evaluate_model(params)

# Perform Sobol sensitivity analysis
Si = sobol.analyze(problem, model_outputs, print_to_console=False)

# Plotting time series of Sobol indices
num_steps = 100  # Number of time steps
time = np.linspace(0, num_steps, num_steps)
plt.figure(figsize=(10, 6))

for i, param_name in enumerate(problem['names']):
    plt.plot(time, Si['S1'][:, i], label=param_name)

plt.xlabel('Time')
plt.ylabel('Sobol Index')
plt.title('Time Series of Sobol Indices')
plt.legend()
plt.grid(True)
plt.show()
