import geopandas as gpd
import matplotlib.pyplot as plt

# Load the GeoJSON file
file_path = '../../InputFiles/Senegal/senegal-with-regions_.geojson'
senegal_regions = gpd.read_file(file_path)
print(senegal_regions.columns)
# Plot the regions, each in a different color
fig, ax = plt.subplots(figsize=(10, 10))
senegal_regions.plot(ax=ax, cmap='Set3', edgecolor='black')

# Add labels to the regions (optional)
# If there is a column with region names, replace 'id' with the name of that column
for idx, row in senegal_regions.iterrows():
    plt.annotate(text=row['id'], xy=(row.geometry.centroid.x, row.geometry.centroid.y),
                 horizontalalignment='center', fontsize=8)

# Set the title and axis labels
plt.title('Regions of Senegal')
plt.xlabel('Longitude')
plt.ylabel('Latitude')

# Remove the axes
plt.axis('off')

# Show the plot
plt.show()
