# -------------------------------- IMPORT -------------------------------------
import postprocess_functions as pp
import numpy as np

# ------------------------------ PARAMETERS -----------------------------------
# Path for output folder where links files are stored
# pathLinkFiles = '/home/cgotelli/Documents/ttga_DEM/output/'

# DEM_imagePath = "/home/cgotelli/Documents/ttga_DEM/toProcess/rescaled_dsm02.png"
postProcessPath = "/home/lhe/Documents/output/output/"

# Delta = 1

# ------------------------------- BOOLEANS ------------------------------------
saveMat = False
plotNetwork = True
printBinary = False
findNodes = True

# ------------------------------- PROCESS -------------------------------------
# pp.savemat_links(postProcessPath)

# links, x_links, y_links = pp.load_matfile(postProcessPath, Delta)

# background, w, h, c = pp.load_background(postProcessPath)

# name = "test" # This should come from the for-loop for each file to postprocess
# binary = pp.make_binary(w, h, x_links, y_links, printBinary, 
#                         postProcessPath, name)


deltas = np.arange(0.2,10,1)
# print(deltas)
count_nodes = []
coords_nodes=[]
for Delta in deltas:
    count_nodesi, coords_nodesi = pp.postprocess(postProcessPath, saveMat, plotNetwork, 
                       printBinary, findNodes, Delta)
    count_nodes.append(count_nodesi)
    coords_nodes.append(coords_nodesi)
