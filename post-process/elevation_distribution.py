# IMPORT ----------------------------------------------------------------------
import math
import numpy as np
from scipy.io import loadmat
import matplotlib.pyplot as plt

#------------------------------------------------------------------------------
#                          Elevations along the link
#------------------------------------------------------------------------------

def links_elevations(DEM, links, Delta):
    
    # extracts elevation values of DEMs detrended for each pixel which is a part
    # of a link at a given delta.
    
    # return a matrix with different elevation values along the links
    
    elev_list = []
    
    with open(DEM, "r") as f:
        line = f.readline()
        for line in f:
            elev_list.append(line.split())
    elevations = np.asarray(elev_list)
    elevations = elevations.astype(np.float)
    rows, columns = np.shape(elevations)
    print(np.shape(elevations))    
    
    data = loadmat(links)
    links = data['links']
    index_link = links[:,0]
    delta_link = links[:,1]
    x = links[:,2]
    y = links[:,3]
    d=0
    
    # taking all the indexes > delta
    while delta_link[d]>=Delta or delta_link[d]=='inf':
        d +=1

    # indexes is a list of lists containing the index lists of each link
    indexes = []
    index_list = []
    for i in range (1,d+1):
        if index_link[i]==index_link[i-1]:
            index_list.append(i)
        else:
            indexes.append(index_list)
            index_list = []
            index_list.append(i)
    
    links_elevations = np.zeros((0,3))
    
    for index in indexes:
        for i in index :
            xi = int(x[i])
            yi = int(y[i])
            if 0 <= xi < columns and 0 <= yi < rows:
                elevation_i = elevations[yi][xi]
                links_elevations = np.append(links_elevations, np.array([[index_link[i],delta_link[i],elevation_i]]), axis = 0)
    
    return links_elevations


#------------------------------------------------------------------------------
#                      Distributions of the elevations
#------------------------------------------------------------------------------

def elevation_distributions(elevations, choice):
    # To choose the plot, modify 'choice' which can be :
    #    --> 'along each link' : to plot the distribution of the elevation along the link
    #    --> 'for different volume parameter scales' : to plot the istribution of the elevation for different volume parameter scales
    
    plt.style.use('seaborn-pastel')

    if choice == 'along each link':
        elevation_list = []
        for i in range (1,len(elevations)):
            if elevations[i][0]==elevations[i-1][0]:
                elevation_list.append(elevations[i][2])
            else :
                elevation_list.append(elevations[i][2])
                plt.hist(elevation_list, bins=20, edgecolor = "grey")
                plt.title('Distribution of the elevation along the link ' + str(int(elevations[i-1][0])) + ' and delta = ' + str('%.3g' % elevations[i-1][1]))
                plt.xlabel('Corrected elevation (m)')
                plt.ylabel('Count')
                plt.show()
                elevation_list = []
            if i == len(elevations)-1:
                plt.hist(elevation_list, bins=20, edgecolor = "grey")
                plt.title('Distribution of the elevation along the link ' + str(int(elevations[i-1][0])) + ' and delta = ' + str('%.3g' % elevations[i-1][1]))
                plt.xlabel('Corrected elevation (m)')
                plt.ylabel('Count')
                plt.show()

    if choice == 'for different volume parameter scales':
        liste = []
        for i in range (1,len(elevations)):
            if elevations[i][0]==elevations[i-1][0]:
                liste.append(elevations[i][2])
            else :
                lab = "delta=" + str('%.3g' % elevations[i - 1][1])
                ax = plt.subplot()
                cm = plt.cm.get_cmap('RdYlBu_r')
                N, bins, patches = ax.hist(liste, label = lab, bins = 20, alpha=0.6, edgecolor = "grey")
                # patches.set_facecolor("red")
                liste = []
                liste.append(elevations[i][2])
            if i == len(elevations)-1:
                lab = "delta=" + str('%.3g' % elevations[i - 1][1])
                ax = plt.subplot()
                cm = plt.cm.get_cmap('RdYlBu_r')
                N, bins, patches = ax.hist(liste, label = lab, bins = 20, alpha=0.6, edgecolor = "grey")
        
        ax.legend(fontsize=8, ncol=2)
        plt.title('Distribution of the elevation for different volume parameter scales')
        plt.xlabel('Elevation (m)')
        plt.ylabel('Count')
        plt.show()
                

    
#------------------------------------------------------------------------------
toProcess_path = '/home/lhe/Documents/ttga_DEM/toProcess/'
detrend_file = 'detrended_dsm01.txt'
mat_file_path = '/home/lhe/Documents/PostProcess/savemat/'
mat_file = 'output_rescaled_dsm01txt_postprocess.mat'

elevations = links_elevations(toProcess_path + detrend_file, mat_file_path + mat_file, 4)
elevation_distributions(elevations, 'for different volume parameter scales')