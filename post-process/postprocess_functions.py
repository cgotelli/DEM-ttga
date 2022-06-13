# IMPORT ----------------------------------------------------------------------
from scipy.io import savemat, loadmat
from os import listdir, mkdir
from os.path import isfile, join, exists
import numpy as np
import matplotlib.pyplot as plt
import cv2

# FUNCTIONS -------------------------------------------------------------------
def load_matfile(matfilePath, Delta):
    links = loadmat(matfilePath)
    links = links ['links']
    
    links = links[links[:,1]>=Delta]
    
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
        
    plt.figure(figsize=(30,10))
    for i in range(len(index_link)):

        # The same index value indicates the same link. We extract its coordinates :
        if index_link[i]==index_link[i-1]:
            X.append(x[i])
            Y.append(y[i])

<<<<<<< Updated upstream
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
=======
# PARAMETERS ------------------------------------------------------------------
matfilePath = "/home/lhe/Documents/PostProcess/savemat/link_seq_test_postprocess.mat"
DEM_imagePath = "/home/lhe/Documents/ttga_DEM/DEMs/rescaled_dsm01.png"
# PROCESS ---------------------------------------------------------------------
>>>>>>> Stashed changes

    ax.imshow(img)
    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height * 0.1,
                 box.width, box.height * 0.9])
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
          fancybox=False, shadow=False, ncol=5)
    
    plt.title('networks ' +r'$\delta_{lim}=$'+' '+str(Delta))
    plt.axis("off")
    plt.show
    
def makeFolder(postProcessPath, process):
    output_path = join(postProcessPath, process)
    if not exists(output_path):
        mkdir(output_path)
    
    
    
    

def make_binary(w, h, x_links, y_links, printBinary, postProcessPath, name):
    
    binary = np.zeros((h, w))
    
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
        saveBinaryPath = join(postProcessPath,str(name+"_binary.png"))
        print(saveBinaryPath)
        fig.savefig(saveBinaryPath, dpi=dpi, transparent=True)
    plt.show()
    
    return binary


