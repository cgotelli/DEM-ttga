# -------------------------------- IMPORT -------------------------------------
import numpy as np
import matplotlib.pyplot as plt 
from PIL import Image, ImageOps
from scipy.io import loadmat
from os.path import join
from math import dist



#------------------------------------------------------------------------------
#                                 Suavización 
#------------------------------------------------------------------------------

def find_nearest(direction, point, links, w, h):

    # for each direction, we take the coordinate that will change depending on
    # the direction and we add to it +/- 1. As long as the new coordinate does 
    # not include in the links, we continue. The function returns the coordinate 
    # of the nearest point once we reach a link, except if we reach the boundary.
    
    # the file links containing the links is the file .mat 
    # w and h are respectively the width and the height of the DEM

    if direction == 'nord' and int(point[1]) < h : # check if the point is not out of the boundaries
        y = int(point[1]) +1 # +1 to go the the north 
        while [int(point[0]),y] not in links.tolist() : # while the new point is not on a link 
            if y < h : # check if the new point is not out of the boundaries
                y += 1 
            else: 
                return 'Boundary reached : no nearest value'
        return int(point[0]),y # return the point once we reach a link

    # repeat the same for the other 3 directions
    if direction == 'sud' and point[1] > 0:
        y = int(point[1]) -1
        while [int(point[0]),y] not in links.tolist() :
            if y > 0:
                y = y - 1
            else:
                return 'Boundary reached : no nearest value'
        return int(point[0]),y

    if direction == 'est' and point[0] < w:
        x = int(point[0]) +1
        while [x,int(point[1])] not in links.tolist() :
            if x < w:
                x += 1
            else:
                return 'Boundary reached : no nearest value'
        return x,int(point[1])

    if direction == 'ouest' and point[0] > 0:
        x = int(point[0]) -1
        while [x,int(point[1])] not in links.tolist() :
            if x > 0:
                x = x - 1
            else: 
                return 'Boundary reached : no nearest value'
        return x,int(point[1])

    else:
        return 'Boundary reached : no nearest value'




def close_gap(point, link, links, w, h):
    
    # close_gap return a matrix which contains the coordinates of the points 
    # used to close the gap between a point and its nearest point in an other link
    
    # the file links is the file .mat 
    # w and h are respectively the width and the height of the DEM
    
    link_gap = np.zeros((0,2))

    #direction nord
    
    if find_nearest('nord', point, links, w, h) != 'Boundary reached : no nearest value':
        # check that the nearest point is not out of the boundaries 
        x_nord, y_nord = find_nearest('nord', point, links, w, h) # take the coordinates of the nearest point
        # check if the nearest point is not in the link 
        while [x_nord, y_nord] in link.tolist(): # if the nearest point is in the link 
            if find_nearest('nord', [x_nord, y_nord], links, w, h) != 'Boundary reached : no nearest value':
                # we continue the search of the nearest point, starting from the previous nearest point
                x_nord, y_nord = find_nearest('nord', [x_nord, y_nord], links, w, h) 
            else:
                break
        # if the nearest point is not in the link, we compute the distance between the point and the nearest point
        dist_nord = dist(point, [x_nord, y_nord]) 
    else: # if we reach the boundary, the distance between the point and the 
          # nearest point contained in the links does not exist (unknown)
        dist_nord = 'unknowm'
    
    # repeat the same for the other 3 directions
    
    #direction est
    if find_nearest('est', point, links, w, h) != 'Boundary reached : no nearest value':
        x_est, y_est = find_nearest('est', point, links, w, h)
        while [x_est, y_est] in link.tolist():
            if find_nearest('est', [x_est, y_est], links, w, h) != 'Boundary reached : no nearest value':
                x_est, y_est = find_nearest('est', [x_est, y_est], links, w, h)
            else:
                break
        dist_est = dist(point, [x_est, y_est])
    else:
        dist_est = 'unknowm'

    #direction sud
    if find_nearest('sud', point, links, w, h) != 'Boundary reached : no nearest value':    
        x_sud, y_sud = find_nearest('sud', point, links, w, h)
        while [x_sud, y_sud] in link.tolist():
            if find_nearest('sud', [x_sud, y_sud], links, w, h) != 'Boundary reached : no nearest value':
                x_sud, y_sud = find_nearest('sud', [x_sud, y_sud], links, w, h)
            else:
                break
        dist_sud = dist(point, [x_sud, y_sud])
    else:
        dist_sud = 'unknowm'

    # direction ouest
    if find_nearest('ouest', point, links, w, h) != 'Boundary reached : no nearest value':    
        x_ouest, y_ouest = find_nearest('ouest', point, links, w, h)
        while [x_ouest, y_ouest] in link.tolist():
            if find_nearest('ouest', [x_ouest, y_ouest], links, w, h) != 'Boundary reached : no nearest value':
                x_ouest, y_ouest = find_nearest('ouest', [x_ouest, y_ouest], links, w, h)
            else:
                break
        dist_ouest = dist(point, [x_ouest, y_ouest])
    else:
        dist_ouest = 'unknowm'
    
    # create a list with all the distances computed in several directions
    l = [x for x in [dist_nord,dist_est,dist_sud, dist_ouest] if x !='unknowm']
    
    if l != []: # if the list is not empty, we compute the minimum distance
        min_dist = min(l)
        
        if min_dist == dist_nord: 
            # we fill the gap between the point and the nearest point by filling the matrix link_gap
            for i in range(0, y_nord - int(point[1])):
                link_gap = np.append(link_gap, np.array([[point[0], int(point[1]) +i]]), axis = 0)
        if min_dist == dist_est:
            for i in range(0, x_est - int(point[0])):
                link_gap = np.append(link_gap, np.array([[int(point[0]) + i, point[1]]]), axis = 0)
        if min_dist == dist_sud:
            for i in range(0, int(point[1])-y_sud):
                link_gap = np.append(link_gap, np.array([[point[0], int(point[1]) - i]]), axis = 0)
        if min_dist == dist_ouest:
            for i in range(0, int(point[0]) - x_ouest):
                link_gap = np.append(link_gap, np.array([[int(point[0]) - i, point[1]]]), axis = 0)
    
    return link_gap




def suavizar(links, Delta, threshold, w, h):
    
    # Function used to smooth the links for a threshold value.
    # A high threshold value will imply a high smoothing
    # Return the coordinates x and y of the smoothed links
    
    # the file links is the file .mat 
    # w and h are respectively the width and the height of the DEM
    
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
            
    # create a matrix which will store the coordinates of the smooth links
    Smooth = np.zeros([0,2])
    
    for index in indexes: # for all index list
        i = index[0] # the first point index of the link
        Smooth_x = [] 
        Smooth_y = []
        #compute the moving average for the link
        while i < index[-1] - threshold + 1:
            x_average = sum(x[i: i + threshold])/threshold
            y_average = sum(y[i: i + threshold])/threshold           
            Smooth_x.append(int(x_average))
            Smooth_y.append(int(y_average))
            i = i + 1
    
        # fill the missing values 
        missing_values = threshold - 1
        link1_x = [x for x in x[index[0]:index[-1]+1]]
        link1_y = [y for y in y[index[0]:index[-1]+1]]
        link2_x = [x for x in Smooth_x[:]]
        link2_y = [x for x in Smooth_y[:]]
        link3 = np.zeros([len(index),2])
            
        if threshold % 2 == 0:
            index_to_complete = int(missing_values/2)+1
        else:
            index_to_complete = int(missing_values/2)+1

        for i in range(0,len(link2_x)):
            link3[i+index_to_complete][0] = link2_x[i]
            link3[i+index_to_complete][1] = link2_y[i]
        
        for i in range(0, index_to_complete):
            link3[i][0] = link1_x[i] 
            link3[i][1] = link1_y[i]
            link3[len(index)-i-1][0] = link1_x[len(link1_x)-i-1]
            link3[len(index)-i-1][1] = link1_y[len(link1_y)-i-1]

        Smooth = np.append(Smooth, link3, axis=0)
    
    Smooth2 = Smooth
    
    # fill the gap
    for index in indexes: # for each index of each link
        # store the coordinates of each point of each link
        link_x = [x for x in Smooth2[index[0]-1:index[-1],0]]
        link_y = [y for y in Smooth2[index[0]-1:index[-1],1]]
        # take the coordinates of the first point and the last point of the link
        point0 = [ link_x[0] , link_y[0] ]
        point1 = [ link_x[-1] , link_y[-1] ]

        # fill the gap between the first and the last points and their nearest points
        if 0<point0[0]<w and 0<point0[1]<h:
            link_gap0 = close_gap(point0, np.transpose(np.array([link_x, link_y])), Smooth2, w, h)
            Smooth = np.append(Smooth,link_gap0, axis=0)
        if 0<point1[0]<w and 0<point1[1]<h:
            link_gap1 = close_gap(point1, np.transpose(np.array([link_x, link_y])), Smooth2, w, h)  
            Smooth = np.append(Smooth,link_gap1, axis=0)
            # in the smooth matrix which contains the smooth links, we add the gap coordinates
        
    return ([row[0] for row in Smooth],[row[1] for row in Smooth])




#------------------------------------------------------------------------------
#                           Number of branches 
#------------------------------------------------------------------------------

binary_path = ''
binary_file = ''
choice = 'selected' # or 'all'
column_selected = [5,151,500]

def compute_nbranches(binary, choice, column_selected):
    
    # Compute the number of branches for different sections
    # The sections can be chosen in 'column_selected' --> choice = 'selected' 
    # otherwise, all the sections are computed --> choice = 'all'
    
    # binary is the binary path 
    
    img= Image.open(binary)
    img = ImageOps.grayscale(img)
    img = np.array(img.convert('L'))
    img[img > 0] = 1
    height, width = np.shape(img)
    plt.imshow(img, cmap = "Greys")
    
    if choice == 'selected':
        for index in column_selected:
            if index > width:
                print('Column index ', index, ' is out of image width')
                return None

        nbranches = np.zeros([0,2])
        for j in column_selected:
            count_branches = 0
            for i in range (0, height):
                if img[i][j]==1:
                    count_branches += 1
            nbranches = np.append(nbranches, [[j, count_branches]], axis=0)
        print(nbranches) 
        return nbranches  
    
    elif choice == 'all':
        nbranches = np.zeros([0,2])
        for j in range (0, width):
            count_branches = 0
            for i in range (0, height):
                if img[i][j]==1:
                    count_branches += 1
            nbranches = np.append(nbranches, [[j, count_branches]], axis=0)
        print(nbranches)   
        return nbranches
    
    # return a matrix containing the sections and number of branches related
    
compute_nbranches(binary_path + binary_file, choice, column_selected)