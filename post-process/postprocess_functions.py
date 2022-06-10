# IMPORT ----------------------------------------------------------------------
from scipy.io import savemat, loadmat
from os import listdir
from os.path import isfile, join
import numpy as np
import matplotlib.pyplot as plt
# FUNCTIONS -------------------------------------------------------------------
def make_binary(w,h,x_links,y_links,printBinary, postProcessPath):
    
    binary = np.zeros((h, w))
    print('building binary mask')
    print(np.shape(binary))
    
    for x,y in zip(x_links,y_links):
        binary[int(y-1),int(x-1)] = 1
    
    
    dpi = 900
    height, width= np.shape(np.squeeze(binary))
    figsize = width / float(dpi), height / float(dpi)

    fig = plt.figure(figsize=figsize)
    ax = fig.add_axes([0, 0, 1, 1])

    # Hide spines, ticks, etc.
    ax.axis('off')

    # Display the image.
    ax.imshow(binary, cmap = 'Greys_r')
     
    
    if printBinary:
        fig.savefig(postProcessPath+"binary"+".png", dpi=dpi, transparent=True)
    plt.show()
    
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
postProcessPath = "/home/cgotelli/Documents/ttga_DEM/output/"


# BOOLEANS --------------------------------------------------------------------

printBinary = True

# PROCESS ---------------------------------------------------------------------

links, x_links, y_links = load_matfile(matfilePath)

w, h, c = load_background(DEM_imagePath)

binary = make_binary(w, h, x_links, y_links, printBinary, postProcessPath)