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
    maxValue = np.nanmax(im_data[im_data != np.nanmax(im_data)])
    
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

def writeFileTTGA(DEM, rows, columns, yres, xres,  name):
    minValue = np.nanmin(DEM)
    maxValue = np.nanmax(DEM[DEM != np.nanmax(DEM)])

    with open(name,'w') as f:
        f.write(str(rows)+' '+ str(columns)+ ' '+str(yres) +' '+ str(xres) 
                +' '+ str(minValue)+' '+ str(maxValue)+'\n')
        for line in DEM:
            np.savetxt(f, line, fmt='%.7f') 
            
            
def Process(originalDEMsPath, toProcessPath, originalRes, resolutionFactor, 
            modelFactor, dpi):
    
    finalRes = originalRes*modelFactor/resolutionFactor
    
    src = rasterio.open("/home/cgotelli/Documents/DEM_images/dsm01.tif")    
    
    originalDEM = src.read()
    originalDEM = np.squeeze(originalDEM)
    originalDEM = np.matrix(originalDEM)
    originalDEM = originalDEM*modelFactor
    columns, rows = np.shape(originalDEM)
    writeFileTTGA(originalDEM, rows, columns, finalRes, 
                  finalRes, 'original.txt')

    rescaledDEM = rescaleDEM(src, resolutionFactor)
    rescaledDEM[rescaledDEM == -32767] = np.float32('nan')
    rescaledDEM = np.matrix(np.squeeze(rescaledDEM))
    rescaledDEM = rescaledDEM*modelFactor
    columns, rows  = np.shape(rescaledDEM)
    writeFileTTGA(rescaledDEM, rows, columns, finalRes,
                  finalRes, 'rescaled.txt')
    
    printDEM(rescaledDEM, dpi, 'DEM_PNG.png')    

        
#%%
originalDEMsPath = '/home/cgotelli/Documents/ttga_DEM/originalDEMs/'
toProcessPath = '/home/cgotelli/Documents/ttga_DEM/toProcess/'
resolutionFactor = 1/10
originalRes = 0.0004    #meters per pixel
modelFactor = 30

dpi = 900

Process(originalDEMsPath, toProcessPath, originalRes, resolutionFactor,
        modelFactor, dpi)