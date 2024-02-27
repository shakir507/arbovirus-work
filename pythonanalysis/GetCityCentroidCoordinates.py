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

# Initialize the geolocator
geolocator = Nominatim(user_agent="senegal_cities")

# Dictionary to store the centroids
city_centroids = {}

# Iterate over the cities and get their centroids
for node, city in Node_to_city_Senegal.items():
    location = geolocator.geocode(f"{city}, Senegal")
    if location:
        city_centroids[node] = (location.latitude, location.longitude)
    else:
        print(f"Could not find location for {city}")

# Save the centroids to a JSON file
with open('../../InputFiles/Senegal/city_centroids.json', 'w') as outfile:
    json.dump(city_centroids, outfile)

# Print the centroids
for node, centroid in city_centroids.items():
    print(f"{Node_to_city_Senegal[node]}: {centroid}")
