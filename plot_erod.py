import matplotlib.pyplot as plt
import xarray as xr

var = xr.open_dataset("geo_em.d01_masked.nc")["EROD"]

for i in range(var.shape[0]):
    for j in range(var.shape[1]):
        plt.pcolormesh(var[i, j, :, :].values)
        plt.savefig(f"EROD_masked_{i}_{j}.png")
        plt.clf()

var = xr.open_dataset("geo_em.d01.nc")["EROD"]

for i in range(var.shape[0]):
    for j in range(var.shape[1]):
        plt.pcolormesh(var[i, j, :, :].values)
        plt.savefig(f"EROD_{i}_{j}.png")
        plt.clf()
