import os
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

input_dir = "../InputFiles/Senegal/"
output_directory_base0 = "../outputdir/"

networktypes_Senegal = ["SmallWorld", "Random", "ScaleFree"]
NetworkFiles = ["NetworkFileHuman" + x for x in networktypes_Senegal]

fn = NetworkFiles[2]

# Create a new figure for each network
fig, ax = plt.subplots(figsize=(8, 8))
fig.suptitle("Network Realization: " + fn)

output_directory = os.path.join(output_directory_base0, "1/")
adjmatrix = pd.read_json(os.path.join(input_dir, fn + ".json"))
adjmatrix = adjmatrix.drop('node', axis=1)

# Create a graph from the adjacency matrix
G = nx.from_numpy_array(adjmatrix.values)

# Compute the degree of each node
degrees = G.degree()

# Plot the network in circular layout
pos = nx.circular_layout(G)
nx.draw(G, pos=pos, with_labels=False, node_size=50, width=1.0)

# Add node labels with degrees
labels = {}
for node, degree in degrees:
    labels[node] = f"{node}\nDegree: {degree}"
nx.draw_networkx_labels(G, pos=pos, labels=labels, font_color="red")

plt.tight_layout()
plt.show()
