# -------------------------------- IMPORT -------------------------------------
import postprocess_functions as pp
from os.path import join

# ------------------------------ PARAMETERS -----------------------------------
# Path for output folder where links files are stored

postProcessPath = "/home/cgotelli/Documents/ttga_DEM/output/"
matfilesPath = join(postProcessPath, "matfiles")

# deltas = np.arange(0.2, 1, 0.1)
deltas = [0.1]


count_nodes = []  # Number of nodes per network (delta)
coords_nodes = []  # List of coordinates for each per network
delta_nodes = []  # List of delta value for each node list
file_names = []  # Name of file to which each node list belongs
network_length = []  # Array for network length for each delta
# ------------------------------- BOOLEANS ------------------------------------
# Booleans for appyling (or not) the different processes
saveMat = True
plotNetwork = True
printBinary = True
includeNodes = True
plotNodeCount = True
computeLength = True
plotLenght = True
plotVolume = True

# ------------------------------- PROCESS -------------------------------------
# We transform to matfile the links *.txt file.
if saveMat:
    pp.makeFolder(postProcessPath, "matfiles")
    pp.savemat_links(postProcessPath)

# List of matfiles inside matfilesPath directory
files = pp.list_matfiles(matfilesPath)

# For each DEM file we apply the processes defined above
for file in files:
    print("Beginning postproces for file: " + file)
    for Delta in deltas:

        links, count_nodesi, coords_nodesi, net_length = pp.postprocess(
            postProcessPath,
            matfilesPath,
            file,
            saveMat,
            plotNetwork,
            printBinary,
            includeNodes,
            computeLength,
            plotVolume,
            plotNodeCount,
            Delta,
        )

        count_nodes.append(count_nodesi)
        coords_nodes.append(coords_nodesi)
        delta_nodes.append(Delta)
        file_names.append(file)
        network_length.append(net_length)

    if plotVolume:
        pp.plot_volume_length(links, postProcessPath, file)

if plotNodeCount:
    print("Here we print the nodes graph evolution")
    pp.plot_nodes(file_names, delta_nodes, count_nodes, postProcessPath)

if plotLenght:
    print("Here we print the network length evolution")
    pp.plot_length(file_names, delta_nodes, network_length, postProcessPath)
