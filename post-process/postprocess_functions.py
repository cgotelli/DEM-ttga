# -------------------------------- IMPORT -------------------------------------
from scipy.io import savemat, loadmat
from os import listdir, mkdir
from os.path import isfile, join, exists
import numpy as np
import matplotlib.pyplot as plt
import cv2

# ------------------------------ FUNCTIONS ------------------------------------
def savemat_links(postProcessPath):
    link_sequence_path = join(postProcessPath, "links_original")
    # List all the link sequences in the path indicated
    files = [f for f in listdir(link_sequence_path) if isfile(join(link_sequence_path, f))]
    
    # For all link sequences in the list
    for link_sequence in files:
        #print(link_sequence)
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
        save_path = join(link_sequence_path,"matfile")
        savemat(save_path+link_sequence[:-4] + '_postprocess.mat', {'links':link})
        
def load_matfile(matfilePath, Delta):
    join(matfilePath, "matfiles")
    links = loadmat(matfilePath)
    links = links ['links']
    
    links = links[links[:,1]>=Delta]
    
    x_links = links[:, 2] 
    y_links = links[:, 3] 
    return links, x_links, y_links

def load_background(DEMpath):
    DEM = plt.imread(DEMpath)
    (h, w,c) = np.shape(DEM)
    return DEM, w, h, c

    
def makeFolder(postProcessPath, process):
    output_path = join(postProcessPath, process)
    if not exists(output_path):
        mkdir(output_path)
    
    
def make_binary(w, h, x_links, y_links, printBinary, postProcessPath, name):
    
    binary = np.zeros((h, w))
    
    for x,y in zip(x_links,y_links):
        binary[int(y-1),int(x-1)] = 1
    
    dpi = 900
    height, width= np.shape(np.squeeze(binary))
    figsize = width / float(dpi), height / float(dpi)

    fig = plt.figure(figsize=figsize)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis('off')
    ax.imshow(binary, cmap = 'Greys_r')
    if printBinary:
        saveBinaryPath = join(postProcessPath,str(name+"_binary.png"))
        fig.savefig(saveBinaryPath, dpi=dpi, transparent=True)
    plt.show()
    
    return binary



def postprocess(postProcessPath, matfile, network, binary):
    print("Beginning postproces")
    if matfile:
        makeFolder(postProcessPath,"matfile")
    if network:
        makeFolder(postProcessPath,"network")
    if binary:
        makeFolder(postProcessPath,"binary")
    
    
