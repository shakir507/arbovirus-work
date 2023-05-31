import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from easyvvuq import Campaign, OutputType
from easyvvuq.parameters.base import Parameter
from easyvvuq.sampling import SobolSampleGenerator
from easyvvuq.analysis import SobolAnalysis
import os
# Define the SIR model equations
def sir_model(y, t, beta, gamma):
    S, I, R = y
    dSdt = -beta * S * I
    dIdt = beta * S * I - gamma * I
    dRdt = gamma * I
    return [dSdt, dIdt, dRdt]

# Define the parameter ranges for sampling
params = {
    "beta": Parameter("beta", type="uniform", bounds=[0.1, 0.5]),
    "gamma": Parameter("gamma", type="uniform", bounds=[0.05, 0.2])
}

# Set up the model evaluation function
def evaluate_model(params):
    # Set initial conditions
    y0 = [0.99, 0.01, 0.0]
    t = np.linspace(0, 100, 100)  # Time grid

    # Solve the SIR model with the given parameters
    solution = odeint(sir_model, y0, t, args=(params["beta"], params["gamma"]))
    return solution[:, 1]  # Return the Infectious (I) compartment

# Set up the Sobol sampling
sampler = SobolSampleGenerator(params, 1000)

# Set up the campaign
campaign = Campaign(name="sobol_campaign", work_dir=os.path.join(os.getcwd(),"SobolUA/"))
campaign.set_app(evaluate_model)
campaign.set_sampler(sampler)

# Define the output parameters to collect
campaign.add_output(OutputType.SOBOL_TOTAL, "beta")
campaign.add_output(OutputType.SOBOL_TOTAL, "gamma")

# Run the campaign
campaign.execute().collate()

# Perform Sobol analysis
analysis = SobolAnalysis(campaign, "sobol_campaign")
analysis.plot_sobol_total_indices()

# Show the plot
plt.show()
