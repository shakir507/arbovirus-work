import numpy as np
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html

# Function to compute Lorenz attractor
def compute_lorenz(x, y, z, sigma, rho, beta):
    dx = sigma * (y - x)
    dy = x * (rho - z) - y
    dz = x * y - beta * z
    return dx, dy, dz

# Set up initial values and parameters
dt = 0.01
num_steps = 5000
t = np.arange(0, num_steps * dt, dt)
x = np.zeros(num_steps)
y = np.zeros(num_steps)
z = np.zeros(num_steps)

sigma = 10.0
rho = 28.0
beta = 8.0 / 3.0

x[0], y[0], z[0] = (1.0, 1.0, 1.0)

# Compute the Lorenz attractor
for i in range(1, num_steps):
    dx, dy, dz = compute_lorenz(x[i-1], y[i-1], z[i-1], sigma, rho, beta)
    x[i] = x[i-1] + dt * dx
    y[i] = y[i-1] + dt * dy
    z[i] = z[i-1] + dt * dz

# Create Dash app
app = dash.Dash(__name__)

# Create Figure object
fig = go.Figure()

# Add scatter plot of Lorenz attractor
fig.add_trace(go.Scatter3d(
    x=x,
    y=y,
    z=z,
    mode='lines',
    line=dict(color='blue', width=2),
    name='Lorenz Attractor'
))

# Set layout options
fig.update_layout(
    scene=dict(
        xaxis=dict(title='X'),
        yaxis=dict(title='Y'),
        zaxis=dict(title='Z')
    ),
    title='Lorenz Attractor Simulation'
)

# Define app layout
app.layout = html.Div([
    dcc.Graph(
        id='lorenz-attractor',
        figure=fig
    )
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
