# IMPORT ----------------------------------------------------------------------
import matplotlib.pyplot as plt 
import numpy as np
from scipy.io import loadmat
import cv2

# PATHS -----------------------------------------------------------------------

# Enter the path of the folder containing the DEMs
DEMs_path = '/home/lhe/Documents/ttga_DEM/DEMs/'

# Enter the path of the folder containing the network links
network_path = '/home/lhe/Documents/PostProcess/savemat/'

# Enter the path of the post processing folder saving the networks plots
save_path = '/home/lhe/Documents/ttga_DEM/output/'

# -----------------------------------------------------------------------------

def compute_nodes (network, Delta):
    data = loadmat(network)
    links = data['links']
    index_link = links[:,0]
    delta_link = links[:,1]
    x = links[:,2]
    y = links[:,3]
    nodes = np.empty([0, 2])
    count_nodes = 0
    d = 0
    while delta_link[d]>=Delta or delta_link[d]=='inf':
        d +=1
    for i in range (0,d):   
        if index_link[i]!=index_link[i-1] or index_link[i]!=index_link[i+1]:
            nodes = np.append(nodes, np.array([[x[i],y[i]]]), axis=0)
    nodes = np.unique(nodes, axis=0)
    for line in nodes:
        count_nodes += 1
    return count_nodes, nodes


def plot_network (DEM, networks, Delta, save_path, nodes):
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

    fig = plt.figure(figsize=(10,10))

    for i in range(1,len(x)):

        # The same index value indicates the same link. We extract its coordinates :
        if index_link[i] == index_link[i-1]:
            X.append(x[i])
            Y.append(y[i])

        else:
        # If the index value change, we plot (X,Y) corresponding to the previous link :
            if delta_link[i-1] > Delta or delta_link[i-1]=='inf':
                lab = 'delta=' + str(delta_link[i-1])
                ax = plt.subplot(111)
                ax.plot(X, Y, label=lab)

            # Then we reset X and Y
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
    if nodes:
        count_nodes, Node = compute_nodes (networks, Delta)
        for line in Node:
            plt.scatter(line[0],line[:][1],color='red')
            plt.title('networks ' +r'$\delta_{lim}=$'+' '+ str(Delta) + '  &   nodes = ' + str(count_nodes))
    else:
        plt.title('networks ' +r'$\delta_{lim}=$'+' '+ str(Delta))
    plt.axis("on")
    plt.show


# PROCESS ---------------------------------------------------------------------
Delta = 1000
plot_network (DEMs_path + '/rescaled_dsm01.png', network_path +
              'output_rescaled_dsm01txt_postprocess.mat', Delta, save_path, True)
compute_nodes (network_path + 'output_rescaled_dsm01txt_postprocess.mat', Delta)