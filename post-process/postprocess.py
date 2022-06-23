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
ordered_nodes = []  # Nodes with ordered [index, xcoord, ycoord]
edges = []  # Edges defined as [start, end] based on ordered nodes' index
extremeNodes = []

# ------------------------------- BOOLEANS ------------------------------------
# Booleans for appyling (or not) the different processes
saveMat = False  # Transform links' .txt files to .mat
plotNetwork = True  # Plot DEM with
plotBinary = True  # Plot
includeNodes = True  # Include nodes in network graph
plotNodeCount = True  # Plot total number of nodes in time. If True, "plotNetwork" must be True
computeLength = True
plotLenght = True  # To plot network length in time. If True, "computeLength" must be True
plotVolume = True
getMatrices = True  # Directed graphs matrices

# ------------------------------- PROCESS -------------------------------------
# We transform to matfile the links *.txt file.
if saveMat:
    pp.makeFolder(postProcessPath, "matfiles")
    pp.savemat_links(postProcessPath)

# List of matfiles inside matfilesPath directory
files = pp.list_matfiles(matfilesPath)

files = sorted(files)  # Sort by name

# For each DEM file we apply the processes defined above
for file in files:

    print("Beginning postproces for file: " + file)
    for Delta in deltas:

        (
            links_original,
            links_filtered,
            count_nodesi,
            coords_nodesi,
            net_length,
            ordered_nodesi,
            edgesi,
            extremeNodesi,
        ) = pp.postprocess(
            postProcessPath,
            matfilesPath,
            file,
            saveMat,
            plotNetwork,
            plotBinary,
            includeNodes,
            computeLength,
            plotVolume,
            plotNodeCount,
            getMatrices,
            Delta,
        )

        count_nodes.append(count_nodesi)
        coords_nodes.append(coords_nodesi)
        delta_nodes.append(Delta)
        file_names.append(file)
        network_length.append(net_length)
        ordered_nodes.append(ordered_nodesi)
        edges.append(edgesi)
        extremeNodes.append(extremeNodesi)

    if plotVolume:
        pp.plot_volume_length(links_original, postProcessPath, file)

if plotNodeCount:
    print("Here we print the nodes graph evolution")
    pp.plot_nodesEvolution(
        file_names, delta_nodes, count_nodes, postProcessPath
    )

if plotLenght:
    print("Here we print the network length evolution")
    pp.plot_Networklength(
        file_names, delta_nodes, network_length, postProcessPath
    )
