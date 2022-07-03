# IMPORT ----------------------------------------------------------------------
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import loadmat
import richdem as rd
from scipy.spatial import distance


#------------------------------------------------------------------------------
#                            Slope computations
#------------------------------------------------------------------------------

def calculate_slope(DEM):
    # compute the slope from a DEM
    
    img = rd.LoadGDAL(DEM)
    slope = rd.TerrainAttribute(img, attrib='slope_riserun')
    rd.rdShow(slope, axes=False, cmap='magma', figsize=(8, 5.5))
    rd.title('Slope [m]')
    plt.show()
    return slope


def links_slope(slope, links, Delta):
    # compute the slope along the links
    
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
    
    # links_slopes contains the slope at each point of the links
    links_slopes = np.zeros((0,5))
    rows, columns = np.shape(slope)
    
    for index in indexes:
        for i in index :
            xi = int(x[i])
            yi = int(y[i])
            if 0 <= xi < columns and 0 <= yi < rows:
                slope_i = slope[yi][xi]
                links_slopes = np.append(links_slopes, np.array([[index_link[i],delta_link[i],xi, yi, slope_i]]), axis = 0)
    
    return links_slopes


#------------------------------------------------------------------------------
#                      Plot slope distribution and profile
#------------------------------------------------------------------------------

def plot_slope(slopes, choice):
    
    # choice can be 'distribution' or 'profile'
    # 'distribution' plots for each link the slope distribution 
    # 'profile' plots for each link the slope profile along the link 
    # slopes is the matrix returned by links_slope containing the links and 
    # the slopes associated
    
    if choice == 'distribution':
        slope_list = []
        for i in range (1,len(slopes)):
            if slopes[i][0]==slopes[i-1][0]:
                if slopes[i][4]!=-9.99900000e+03:
                    slope_list.append(slopes[i][4])
            else :
                plt.hist(slope_list, bins=20, edgecolor = "grey")
                plt.title('Distribution of the slopes for the link ' + str(int(slopes[i-1][0])) + ' and delta = ' + str('%.3g' % slopes[i-1][1]))
                plt.xlabel('Slopes')
                plt.ylabel('Count')
                plt.show()
                slope_list = []
                if slopes[i][4]!=-9.99900000e+03:
                    slope_list.append(slopes[i][4])
            if i==len(slopes)-1:
                plt.hist(slope_list, bins=20, edgecolor = "grey")
                plt.title('Distribution of the slopes for the link ' + str(int(slopes[i-1][0])) + ' and delta = ' + str('%.3g' % slopes[i-1][1]))
                plt.xlabel('Slopes')
                plt.ylabel('Count')
                plt.show()

    
    if choice == 'profile':
        slope_list = []        
        x_cum = [0]
        for i in range (1,len(slopes)):
            if slopes[i][0]==slopes[i-1][0]:
                if slopes[i][4]!=-9.99900000e+03:
                    slope_list.append(slopes[i][4])
                    x_cum.append(x_cum[-1] + distance.euclidean( [ slopes[i-1][2], slopes[i-1][3] ], [ slopes[i][2], slopes[i][3] ]))
            else :
                del x_cum[0]
                plt.plot(x_cum, slope_list)
                plt.title('Slope profile along the link ' + str(int(slopes[i-1][0])) + ' and delta = ' + str('%.3g' % slopes[i-1][1]))
                plt.xlabel('x (m)')
                plt.ylabel('Slope')
                plt.show()
                slope_list = []
                x_cum = [0]
                if slopes[i][4]!=-9.99900000e+03:
                    slope_list.append(slopes[i][4])
                    x_cum.append(x_cum[-1] + distance.euclidean( [ slopes[i+1][2], slopes[i+1][3] ], [ slopes[i][2], slopes[i][3] ]))
            if i==len(slopes)-1:
                del x_cum[0]
                plt.plot(x_cum, slope_list)
                plt.title('Slope profile along the link ' + str(int(slopes[i-1][0])) + ' and delta = ' + str('%.3g' % slopes[i-1][1]))
                plt.xlabel('x (m)')
                plt.ylabel('Slope')
                plt.show()


# --------------------------------- Tests -------------------------------------

path_DEM = '/home/lhe/Documents/ttga_DEM/originalDEMs/'
DEM = 'dsm01.tif'

mat_file_path = '/home/lhe/Documents/PostProcess/savemat/'
mat_file = 'output_rescaled_dsm01txt_postprocess.mat'

print(plot_slope(links_slope(calculate_slope(path_DEM + DEM), mat_file_path + mat_file, 4), 'profile'))
