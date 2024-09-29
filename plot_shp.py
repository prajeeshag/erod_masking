import geopandas as gpd
import matplotlib.pyplot as plt


def plot_shapefile(shapefile):
    # Load the shapefile
    shapefile_gdf = gpd.read_file(shapefile)

    # Plot the shapefile
    shapefile_gdf.plot()

    # Add title and labels
    plt.title("Shapefile Plot")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")

    # Display the plot
    plt.savefig("plot.png")


# Example usage:
shapefile = "iq.shp"
plot_shapefile(shapefile)
