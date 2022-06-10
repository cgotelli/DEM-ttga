# IMPORT ----------------------------------------------------------------------
from scipy.io import savemat, loadmat
from os import listdir
from os.path import isfile, join
import numpy as np

# FUNCTION --------------------------------------------------------------------
def savemat_links(link_sequence_path, save_path):
    
    # List all the link sequences in the path indicated
    files = [f for f in listdir(link_sequence_path) if isfile(join(link_sequence_path, f))]
    
    # For all link sequences in the list
    for link_sequence in files:
    
        # Read of the first line which contains the number of links
        seq = open (link_sequence_path + '/' + link_sequence, 'r')
        number_links = seq.readline()

        # Creation of the link matrix
        link = np.zeros([0,4])
    
        # For all links, we want to have a list of the strings of each line  
        for line in seq:
            add_list = ''   # string to add in the list
            list_line = []  # list of the strings of the line
    
            # For each character of the line :
            # if this one is not a delimiter space, we add it in add_list
            # else, we append the string 'add_list' in the list_line
            for i in range(len(line)):
                if line[i]!=' ':
                    add_list = add_list + str(line[i])
                else :
                    list_line.append(add_list)
                    add_list = ''
                if i == len(line) -1:
                    list_line.append(add_list)
            
            # Define the index link and the delta related to the link
            index_link = list_line[0]
            delta_link = list_line[1]
          
            # Fill the link matrix
            k=2
            while k < len(list_line):
                row = np.zeros(4)
                row[0] = index_link
                row[1] = delta_link
                row[2] = list_line[k]
                row[3] = list_line[k+1]
                link = np.append(link,[row],axis= 0)
                k = k + 2 

        # Save in a .mat file     
        savemat(save_path + '/' + link_sequence[:-4] + '_postprocess.mat', {'links':link})


# PROCESS ---------------------------------------------------------------------        

pathLinkFiles = '/home/cgotelli/Documents/ttga_DEM/output/'
pathSaveMat = '/home/cgotelli/Documents/ttga_DEM/output/matfiles/'

savemat_links(pathLinkFiles, pathSaveMat)