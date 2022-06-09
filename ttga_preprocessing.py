# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import os
import rasterio
from rasterio.plot import show
from rasterio.enums import Resampling

import numpy as np
import shapely.geometry
import geopandas as gpd
import glob
import richdem as rd
import scipy.ndimage
import matplotlib.pyplot as plt


def rescaleDEM(DEM, scaleFactor):
    with DEM as dataset:
        # resample data to target shape
        data = dataset.read(
            out_shape=(dataset.count, int(dataset.height * scaleFactor),
                int(dataset.width * scaleFactor)),resampling=Resampling.bilinear)
    return np.squeeze(data)
    
def printDEM(im_data, dpi, name):
    minValue = np.nanmin(im_data)
    maxValue = maxValue = np.nanmax(im_data[im_data != np.nanmax(im_data)])
    
    height, width= np.shape(np.squeeze(im_data))
    figsize = width / float(dpi), height / float(dpi)

    fig = plt.figure(figsize=figsize)
    ax = fig.add_axes([0, 0, 1, 1])

    # Hide spines, ticks, etc.
    ax.axis('off')

    # Display the image.
    ax.imshow(im_data, vmin=minValue, vmax=maxValue, interpolation='nearest', cmap = 'Greys_r')


    fig.savefig(name, dpi=dpi, transparent=True)
    plt.show()


def writeFileTTGA(mat, name):
    with open(name,'wb') as f:
        for line in mat:
            np.savetxt(f, line, fmt='%.7f') 
            
            
def Process(originalDEMsPath, toProcessPath, originalRes, scaleFactor, 
            dpi):
    
    
    
    src = rasterio.open("/home/cgotelli/Documents/DEM_images/dsm01.tif")    
    
    originalDEM = src.read()
    originalDEM = np.squeeze(originalDEM)
    originalDEM = np.matrix(originalDEM)
    writeFileTTGA(originalDEM, 'original.txt')

    rescaledDEM = rescaleDEM(src, scaleFactor)
    rescaledDEM[rescaledDEM == -32767] = np.float32('nan')
    rescaledDEM = np.matrix(np.squeeze(rescaledDEM))
    writeFileTTGA(rescaledDEM, 'rescaled.txt')
    
    printDEM(rescaledDEM, dpi, 'DEM_PNG.png')    

        
#%%
originalDEMsPath = '/home/cgotelli/Documents/ttga_DEM/originalDEMs/'
toProcessPath = ''
scaleFactor = 1/10
originalRes = 0.0004    #meters per pixel
dpi = 900

Process(originalDEMsPath, toProcessPath, originalRes, scaleFactor, dpi)