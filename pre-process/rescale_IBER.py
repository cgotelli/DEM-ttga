#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 20 09:00:18 2022

@author: epfl-lhe
"""

from contextlib import contextmanager  

import rasterio
from rasterio import Affine, MemoryFile
from rasterio.enums import Resampling
import numpy as np

# use context manager so DatasetReader and MemoryFile get cleaned up automatically
# @contextmanager
def resample_raster(raster, scaleHeight=40, scaleResolution = 1/2):
    t = raster.transform

    # rescale the metadata
    transform = Affine(t.a * scaleHeight/scaleResolution, t.b, t.c, t.d, t.e * scaleHeight/scaleResolution, t.f)
    height = int(raster.height * scaleResolution)
    width = int(raster.width * scaleResolution)

    profile = raster.profile
    profile.update(transform=transform, driver='GTiff', height=height, width=width)

    data = raster.read( # Note changed order of indexes, arrays are band, row, col order not row, col, band
            out_shape=(raster.count, height, width),
            resampling=Resampling.bilinear,
        )
    data[data == -32767] = np.float32(0.2)
    data = data*scaleHeight
    with rasterio.open(
        r'/mnt/data2/20220719/halle_water_20220719-03_20220719T1649_dsm-rescaled.tif',
        'w',
        driver=raster.driver,
        height=height,
        width=width,
        count=raster.count,
        crs = raster.crs,
        nodata = raster.nodata,
        transform = transform,
        dtype = np.float32,
    ) as dest_file:
        dest_file.write(data)
    dest_file.close()
    
    # with MemoryFile() as memfile:
    #     with memfile.open(**profile) as dataset: # Open as DatasetWriter
    #         dataset.write(data)
    #         del data

    #     with memfile.open() as dataset:  # Reopen as DatasetReader
    #         yield dataset  # Note yield not return     

    return data

from rasterio.plot import show
src  = rasterio.open('/mnt/data2/20220719/halle_water_20220719-03_20220719T1649_dsm.tif')

data = resample_raster(src)
show(data)



    
    # with resample_raster(src) as resampled:
    #     print('Orig dims: {}, New dims: {}'.format(src.shape, resampled.shape))
    #     print(repr(resampled))