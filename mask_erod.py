from pathlib import Path

import geopandas as gpd
import numpy as np
import typer
import xarray as xr
from shapely.geometry import Point

app = typer.Typer(pretty_exceptions_show_locals=False)


@app.command()
def mask_netcdf_with_shapefile(geo_em_file: Path, shapefile: Path, output_file: Path):
    # Open the netCDF file

    ds = xr.open_dataset(geo_em_file)

    # Load the shapefile
    shapefile_gdf = gpd.read_file(shapefile)

    # Extract the variable to be masked and the 2D lat/lon
    variable = ds["EROD"]  # Replace with your actual variable name
    # Get the coordinates (lat, lon) from the netCDF data
    lon = ds["XLONG_M"][0, :, :].squeeze().values
    lat = ds["XLAT_M"][0, :, :].squeeze().values

    # Flatten the 2D lat/lon arrays into 1D
    lon_flat = lon.flatten()
    lat_flat = lat.flatten()

    # Create a 1D mask array initialized to False (meaning outside the region)
    mask = np.zeros(lon_flat.shape, dtype=bool)

    # Iterate over all the points in the shapefile and set the mask to True where the point is inside the region
    for polygon in shapefile_gdf.geometry:
        for i in range(lon_flat.shape[0]):
            point = Point(lon_flat[i], lat_flat[i])
            if polygon.contains(point):
                mask[i] = True

    # Reshape the mask back into 2D
    mask_2d = mask.reshape(lon.shape)

    # Apply the mask to the variable (where mask is False, set the variable to NaN)
    for t in range(variable.shape[0]):
        for z in range(variable.shape[1]):
            variable.values[t, z, :, :] = np.where(
                mask_2d, 0, variable.values[t, z, :, :]
            )

    # Save the masked variable back to a new netCDF file
    encode = {}
    for var in ds.data_vars:
        if var == "Times":
            encode[var] = {
                "char_dim_name": "DateStrLen",
                "zlib": True,
            }
            continue
        encode[var] = {"_FillValue": None}
    ds.to_netcdf(output_file, format="NETCDF4", encoding=encode)

    print(f"Masked data saved to {output_file}")


if __name__ == "__main__":
    app()

# Example usage:
geo_em_file = "geo_em.d01.nc"
shapefile = "iq.shp"
output_file = "geo_em.d01_masked.nc"

mask_netcdf_with_shapefile(geo_em_file, shapefile, output_file)
