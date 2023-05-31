import os
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

input_dir = "../InputFiles/Senegal/"
output_directory_base0 = "../outputdir/"

networktypes_Senegal = ["SmallWorld", "Random", "ScaleFree"]
NetworkFiles=["NetworkFileHuman"+x for x in networktypes_Senegal]
num_networks = len(networktypes_Senegal)

# Calculate the number of rows and columns for subplots
num_rows = int(num_networks ** 0.5+1)
num_cols = int((num_networks + num_rows - 1) / num_rows)

# Create the subplots grid
fig, axes = plt.subplots(num_rows, num_cols, figsize=(12, 12))
fig.suptitle("Different Networks Realizations")

Node_to_city_Senegal = {
    0: "Dakar", 1: "Touba", 2: "Thiès", 3: "Rufisque", 4: "Kaolack",
    5: "M'Bour", 6: "Ziguinchor", 7: "Saint-Louis", 8: "Diourbel",
    9: "Louga", 10: "Tambacounda", 11: "Richard Toll", 12: "Kolda",
    13: "Mbacké", 14: "Tivaouane", 15: "Joal-Fadiouth", 16: "Kaffrine",
    17: "Dahra", 18: "Bignona", 19: "Fatick", 20: "Dagana", 21: "Bambey",
    22: "Vélingara", 23: "Sédhiou", 24: "Sébikhotane", 26: "Kédougou",
    26: "Nguékhokh", 27: "Kayar", 28: "Pout", 29: "Mékhé", 31: "Matam",
    31: "Ouro Sogui", 32: "Nioro du Rip", 33: "Kébémer", 34: "Koungheul",
    35: "Guinguinéo", 36: "Bakel", 37: "Mboro", 38: "Linguère", 39: "Sokone",
    40: "Goudomp", 41: "Thiadiaye", 42: "Ndioum", 43: "Diamniadio",
    44: "Khombole", 45: "Gossas", 46: "Kanel"
}

for i, fn in enumerate(NetworkFiles):
    output_directory = os.path.join(output_directory_base0, "1/")
    adjmatrix = pd.read_json(os.path.join(input_dir, fn+".json"))
    
    # Convert adjacency matrix to edge list DataFrame
    edge_list = adjmatrix.stack().reset_index()
    edge_list.columns = ["source", "target", "weight"]
    
    # Create a graph from the edge list DataFrame
    G = nx.from_pandas_edgelist(edge_list, "source", "target", ["weight"])
    
    # Get the subplot axes
    if num_networks > 1:
        ax = axes[i // num_cols, i % num_cols]
    else:
        ax = axes

    # Plot the network
    pos = nx.spring_layout(G)
    nx.draw(G, pos=pos, with_labels=True, ax=ax, node_size=50, width=1.0, style="dashed")

    # Add node labels
    nx.draw_networkx_labels(G, pos=pos, ax=ax, font_color="red")

    ax.set_title(fn)

# Remove any extra empty subplots
if num_networks < num_rows * num_cols:
    if num_networks > 1:
        for i in range(num_networks, num_rows * num_cols):
            fig.delaxes(axes[i // num_cols, i % num_cols])
    else:
        fig.delaxes(axes)
plt.legend(Node_to_city_Senegal)
plt.tight_layout()
plt.show()
