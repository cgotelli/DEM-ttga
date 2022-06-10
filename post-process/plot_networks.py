# IMPORT ----------------------------------------------------------------------
import matplotlib.pyplot as plt 
from scipy.io import loadmat
import cv2

# PATHS -----------------------------------------------------------------------

# Enter the path of the folder containing the DEMs
DEMs_path = '/home/lhe/Documents/ttga_DEM/DEMs'

# Enter the path of the folder containing the network links
network_path = '/home/lhe/Documents/PostProcess/savemat'

# Enter the path of the post processing folder saving the networks plots
save_path = '/home/lhe/Documents/PostProcess/NetworkPlots'

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

    for i in range(len(index_link)):

        # The same index value indicates the same link. We extract its coordinates :
        if index_link[i]==index_link[i-1]:
            X.append(x[i])
            Y.append(y[i])

        else:
        # If the index value change, we plot (X,Y) corresponding to the previous link :
            if delta_link[i] > Delta or delta_link[i]=='inf':
                lab = 'delta=' + str(delta_link[i-1])
                plt.plot(X, Y, label=lab)
            # Then we reset X amd Y
            X = []
            Y = []
            X.append(x[i])
            Y.append(y[i])

    plt.imshow(img)
    plt.title('networks ' +r'$\delta_{lim}=$'+' '+str(Delta))
    plt.show


# PROCESS ---------------------------------------------------------------------
Delta = 1
plot_network (DEMs_path + '/rescaled_dsm01.png', network_path +
              '/output_rescaled_dsm01txt_postprocess.mat', Delta)
