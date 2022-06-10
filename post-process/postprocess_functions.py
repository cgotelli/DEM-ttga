# IMPORT ----------------------------------------------------------------------
from scipy.io import savemat, loadmat
from os import listdir
from os.path import isfile, join
import numpy as np
import matplotlib.pyplot as plt
# FUNCTIONS -------------------------------------------------------------------
def make_binary(w,h,x_links,y_links):
    
    binary = np.zeros((h, w))
    print('building binary mask')
    print(np.shape(binary))
    for x,y in zip(x_links,y_links):
        binary[int(y-1),int(x-1)] = 1
    
    
    plt.imshow(binary, cmap = "Greys_r")
    # plt.plot(x_links,y_links, '.', markersize = .05)
    plt.axis("off")
    
    # binary_mask
    return binary

def load_matfile(matfilePath):
    links = loadmat(matfilePath)
    links = links ['links']
    x_links = links[:, 2] 
    y_links = links[:, 3] 
    return links, x_links, y_links

def load_background(DEMpath):
    DEM = plt.imread(DEMpath)
    (h, w,c) = np.shape(DEM)
    return w, h, c

# PARAMETERS ------------------------------------------------------------------
matfilePath = "/home/cgotelli/Documents/ttga_DEM/output/matfiles/links01_postprocess.mat"
DEM_imagePath = "/home/cgotelli/Documents/ttga_DEM/toProcess/rescaled_dsm02.png"
# PROCESS ---------------------------------------------------------------------

links, x_links, y_links = load_matfile(matfilePath)

w, h, c = load_background(DEM_imagePath)

binary = make_binary(w,h,x_links,y_links)