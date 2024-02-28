import geopandas as gpd
import matplotlib.pyplot as plt
import requests
from geopy.geocoders import Nominatim
import json
# Dictionary of cities in Senegal
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

# To read the centroids of senegal cities from the JSON file
with open('../../InputFiles/Senegal/city_centroids.json', 'r') as infile:
    city_centroids = json.load(infile)

# Convert the keys back to integers (JSON keys are always strings)
city_centroids= {int(k): v for k, v in city_centroids.items()}

# # Print the centroids
# for node, centroid in city_centroids.items():
#     print(f"{Node_to_city_Senegal[node]}: {centroid}")


# Load the GeoJSON file
file_path = '../../InputFiles/Senegal/senegal-with-regions_.geojson'
senegal_regions = gpd.read_file(file_path)
print(senegal_regions.columns)

# Plot the regions
fig, ax = plt.subplots(figsize=(10, 10))
senegal_regions.plot(ax=ax, cmap='Set3', edgecolor='black')

# Plot the city centroids
for node, centroid in city_centroids.items():
    ax.scatter(centroid[1], centroid[0], color='red', label=Node_to_city_Senegal[node])

# Add labels for the cities
for node, centroid in city_centroids.items():
    ax.text(centroid[1], centroid[0], Node_to_city_Senegal[node], fontsize=8)

# Set plot title and labels
ax.set_title('Regions and Cities of Senegal')
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')

# Show the plot
plt.show()
