# -------------------------------- IMPORT -------------------------------------
from scipy.io import savemat, loadmat
from os import listdir, mkdir
from os.path import isfile, join, exists
import numpy as np
import matplotlib.pyplot as plt
import cv2


# ------------------------------- FUNCTIONS -----------------------------------

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

# -----------------------------------------------------------------------------

def plot_node(matfilesPath):
    
    deltas = np.arange(1,40,1)
    
    files = [f for f in listdir(matfilesPath) if isfile(join(matfilesPath, f))]
    print(files)
    
    for delta in deltas:
        nodes = []
        name_files = []
        for file in files:
            count_nodes, Node = compute_nodes(file, delta)
            nodes.append(count_nodes)
            name_files.append(file)
        plt.plot(name_files, nodes)
    plt.title('Count nodes')
    plt.axis("on")
    plt.show


def plot_length(matfilesPath):
    
    deltas = np.arange(1,40,1)
    
    files = [f for f in listdir(matfilesPath) if isfile(join(matfilesPath, f))]
    print(files)
    
    for delta in deltas:
        lengths = []
        name_files = []
        for file in files:
            length = network_length(file, delta)
            lengths.append(length)
            name_files.append(file)
        plt.plot(name_files, lengths)
    plt.title('Network length')
    plt.xlabel('DEM files')
    plt.axis("on")
    plt.show

plot_node('/home/lhe/Documents/output/output/matfiles/')
plot_length('/home/lhe/Documents/output/output/matfiles/')