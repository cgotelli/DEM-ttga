# IMPORT ----------------------------------------------------------------------
import matplotlib.pyplot as plt 
from scipy.io import loadmat
import cv2

# PATHS -----------------------------------------------------------------------

# Enter the path of the folder containing the DEMs
DEMs_path = '/home/cgotelli/Documents/ttga_DEM/toProcess/'

# Enter the path of the folder containing the network links
network_path = '/home/cgotelli/Documents/ttga_DEM/output/matfiles/'

# Enter the path of the post processing folder saving the networks plots
save_path = '/home/cgotelli/Documents/ttga_DEM/output/'

# -----------------------------------------------------------------------------

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


# PROCESS ---------------------------------------------------------------------
Delta = 1
plot_network (DEMs_path + '/rescaled_dsm01.png', network_path +
              '/links01_postprocess.mat', Delta)
