# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import rasterio
from rasterio.plot import show
import numpy as np
import shapely.geometry
import geopandas as gpd
import glob
import richdem as rd
import scipy.ndimage
import matplotlib.pyplot as plt

from rasterio.enums import Resampling
#%%
src = rasterio.open("/home/cgotelli/Desktop/DEM.tif")
src.meta
src.count
# show(src)
show(src, cmap="Greys_r")
r = src.read()

r2 = r[0, :, :]

mat = np.matrix(r2)


with open('outfile.txt','wb') as f:
    for line in mat:
        np.savetxt(f, line, fmt='%.2f')


upscale_factor = 1/8

with src as dataset:

    # resample data to target shape
    data = dataset.read(
        out_shape=(
            dataset.count,
            int(dataset.height * upscale_factor),
            int(dataset.width * upscale_factor)
        ),
        resampling=Resampling.bilinear
    )

    # scale image transform
    transform = dataset.transform * dataset.transform.scale(
        (dataset.width / data.shape[-1]),
        (dataset.height / data.shape[-2])
    )
    
mat = np.matrix(data[0,:,:])*30


with open('outfile2.txt','wb') as f:
    for line in mat:
        np.savetxt(f, line, fmt='%.2f')