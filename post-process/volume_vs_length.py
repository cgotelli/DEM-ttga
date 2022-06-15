# -------------------------------- IMPORT -------------------------------------
from scipy.io import loadmat
import numpy as np
import matplotlib.pyplot as plt 

# PATHS -----------------------------------------------------------------------

# Enter the path of the folder containing the network links
network_path = '/home/cgotelli/Documents/ttga_DEM/output/matfiles/'

# Enter the path of the post processing folder saving the networks plots
save_path = '/home/cgotelli/Documents/ttga_DEM/output/'

def link_length(x,y):
    length = 0
    for i in range(1,len(x)):		
        length += np.sqrt( (x[i]-x[i-1])**2 + (y[i]-y[i-1])**2 )
    return length

def network_length(network, Delta):
    data = loadmat(network)
    links = data['links']
    index_link = links[:,0]
    delta_link = links[:,1]
    x = links[:,2]
    y = links[:,3]
    X = []
    Y = []
    length = 0
    d = 0
    while delta_link[d]>=Delta or delta_link[d]=='inf':
        d +=1
    for i in range (1,d+1):   
        if index_link[i]==index_link[i-1]:
            X.append(x[i])
            Y.append(y[i])
        else:
            length += link_length(X,Y)
            X = []
            Y = []
            X.append(x[i])
            Y.append(y[i])
        
    return length


def plot_volume_length(network):
    data = loadmat(network)
    links = data['links']
    delta_link = links[:,1]
    delta = []
    length = []
    for i in range(1,len(delta_link)):
       if delta_link[i]!=delta_link[i-1] and delta_link[i] > 0.00005:
           delta.append(delta_link[i-1])
           length.append(network_length(network, delta_link[i-1]))
    plt.plot(delta,length)
    plt.xscale("log")
    plt.yscale("log")
    plt.title('Network length')
    plt.xlabel(r'$\delta$')
    plt.ylabel('Network length')
    plt.axis("on")
    plt.show 

plot_volume_length(network_path + 'links01.mat')
