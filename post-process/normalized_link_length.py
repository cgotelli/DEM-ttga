# -------------------------------- IMPORT -------------------------------------
from scipy.io import loadmat
import numpy as np
import matplotlib.pyplot as plt 


#------------------------------------------------------------------------------
#                                Link length 
#------------------------------------------------------------------------------

def link_length(x,y):
    length = 0
    for i in range(1,len(x)):	
        length += np.sqrt( (x[i]-x[i-1])**2 + (y[i]-y[i-1])**2 )
    return length


#------------------------------------------------------------------------------
#                              Network length 
#------------------------------------------------------------------------------

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
    link_lengths =[]
    d = 0
    while delta_link[d]>=Delta or delta_link[d]=='inf':
        d +=1
    for i in range (1,d+1):   
        if index_link[i]==index_link[i-1]:
            X.append(x[i])
            Y.append(y[i])
        else:
            length += link_length(X,Y)
            link_lengths.append(link_length(X,Y))
            X = []
            Y = []
            X.append(x[i])
            Y.append(y[i])

    return length, link_lengths


#------------------------------------------------------------------------------
#                             Normalized length 
#------------------------------------------------------------------------------

def normalized_lengths(links, Delta):
    data = loadmat(links)
    links = data['links']
    index_link = links[:,0]
    delta_link = links[:,1]
    x = links[:,2]
    y = links[:,3]

    # each row of normalized_length contains the link index and the normalized length
    normalized_length = np.zeros((0,2))
    norm_cumulative_length = 0
    
    d = 0
    while delta_link[d]>=Delta or delta_link[d]>=Delta:
        d +=1

    X0 = []
    Y0 = []
    i=0
    while index_link[i]==0:
        X0.append(x[i])
        Y0.append(y[i])
        i += 1
    lowest_length = link_length(X0, Y0)
    
    X = []
    Y = []
    for j in range (0,d):   
        if index_link[j+1]==index_link[j]:
            X.append(x[j])
            Y.append(y[j])
        else:
            X.append(x[j])
            Y.append(y[j])
            normalized_length = np.append(normalized_length, np.array([[index_link[j], link_length(X,Y)/lowest_length]]), axis =0)
            norm_cumulative_length += link_length(X,Y)/lowest_length
            X = []
            Y = []
    
    return normalized_length, norm_cumulative_length


#------------------------------------------------------------------------------
#                             Plot distribution 
#------------------------------------------------------------------------------

def plot_distribution(link_lengths, normalized_lengths):
    plt.hist(link_lengths, bins=7, density=False)
    if normalized_lengths == True:
        plt.title('Distribution of the normalized link lengths')
        plt.xlabel('Link length')
    else:
        plt.title("Distribution of the link lengths")
        plt.xlabel('Link length (m)')
    plt.ylabel('Count')
    plt.show()
    return None

# Enter the path of the folder containing the network links
network_path = '/home/lhe/Documents/PostProcess/savemat/'
network_file = 'output_rescaled_dsm01txt_postprocess.mat'


# -------------------------------- TESTS --------------------------------------

#print(network_length(network_path + network_file, 1))
#print(normalized_lengths(network_path + network_file, 1))
length, link_lengths = network_length(network_path + network_file, 0.1)
normalized_length, norm_cumulative_length = normalized_lengths(network_path + network_file, 0.0001)
print(plot_distribution(normalized_length[:,1], True))