# IMPORT ----------------------------------------------------------------------
from scipy.io import savemat, loadmat
from os import listdir
from os.path import isfile, join
import numpy as np
import matplotlib.pyplot as plt
import cv2

# FUNCTIONS -------------------------------------------------------------------
def make_binary(w, h, x_links, y_links, printBinary, postProcessPath):
    
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
    ax.axis('off')
    ax.imshow(binary, cmap = 'Greys_r')
    if printBinary:
        fig.savefig(postProcessPath+"binary"+".png", dpi=dpi, transparent=True)
    plt.show()
    
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
    return DEM, w, h, c

def plot_network (DEM, networks, Delta):
    # Read the .mat file and the DEM :
    data = loadmat(networks)
    img = cv2.imread(DEM)
    links = data['links']
    
    # Extract each column of the links matrix :
    index_link = links[:,0]
    delta_link = links[:,1]
    x = links[:,2]
    y = links[:,3]
    
    # Create two arrays that will be used to plot each link :
    X = []
    Y = []
        
    fig = plt.figure(figsize=(30,10))
    for i in range(len(index_link)):

        # The same index value indicates the same link. We extract its coordinates :
        if index_link[i]==index_link[i-1]:
            X.append(x[i])
            Y.append(y[i])

        else:
        # If the index value change, we plot (X,Y) corresponding to the previous link :
            if delta_link[i] > Delta or delta_link[i]=='inf':
                lab = 'delta=' + str(delta_link[i-1])
                ax = plt.subplot(111)
                ax.plot(X, Y, label=lab)
                
            # Then we reset X amd Y
            X = []
            Y = []
            X.append(x[i])
            Y.append(y[i])

    ax.imshow(img)
    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height * 0.1,
                 box.width, box.height * 0.9])
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
          fancybox=False, shadow=False, ncol=5)
    
    plt.title('networks ' +r'$\delta_{lim}=$'+' '+str(Delta))
    plt.axis("off")
    plt.show
    
# PARAMETERS ------------------------------------------------------------------
matfilePath = "/home/cgotelli/Documents/ttga_DEM/output/matfiles/links01_postprocess.mat"
DEM_imagePath = "/home/cgotelli/Documents/ttga_DEM/toProcess/rescaled_dsm02.png"
postProcessPath = "/home/cgotelli/Documents/ttga_DEM/output/"


# BOOLEANS --------------------------------------------------------------------

printBinary = True


# PROCESS ---------------------------------------------------------------------


links, x_links, y_links = load_matfile(matfilePath)
background, w, h, c = load_background(DEM_imagePath)

binary = make_binary(w, h, x_links, y_links, printBinary, postProcessPath)