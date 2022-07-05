# -------------------------------- IMPORT -------------------------------------
import postprocess_functions as pp
from os.path import join
import numpy as np

# ------------------------------ PARAMETERS -----------------------------------
# Path for output folder where links files are stored

postProcessPath = "/mnt/data2/DEMtest/output/"
matfilesPath = join(postProcessPath, "matfiles")

# deltas = np.arange(0.2, 1, 0.1)
deltas = [450]
smoothWindow = 30
choice = "all"  # or 'all'
columns_selected = [5, 151, 500]
dt = 0.02
delta_T = 0.2


count_nodes = []  # Number of nodes per network (delta)
coords_nodes = []  # List of coordinates for each per network
delta_nodes = []  # List of delta value for each node list
file_names = []  # Name of file to which each node list belongs
network_length = []  # Array for network length for each delta
ordered_nodes = []  # Nodes with ordered [index, xcoord, ycoord]
edges = []  # Edges defined as [start, end] based on ordered nodes' index
extremeNodes = []
w = 646
h = 564

# ------------------------------- BOOLEANS ------------------------------------
# Booleans for appyling (or not) the different processes

saveMat = False  # Transform links' .txt files to .mat
plotNetwork = True  # Plot DEM with
plotBinary = True  # Plot binary image
smoothChannels = False  # For smoothing channel network
includeNodes = True  # Include nodes in network graph
# Plot total number of nodes in time. If True, "plotNetwork" must be True
plotNodeCount = True
computeLength = True
# To plot network length in time. If True, "computeLength" must be True
plotTotalLength = False
plotDeltavsLength = False
getMatrices = True  # Directed graphs matrices
directedGraphs = False
saveGraphs = True
computeBraidingIndex = True

DEMtimeAverage = False
DEMensembleAverage = False

ElevationDistribution = False
# 'along each link': to plot the distribution of the elevation along the link
# 'for different volume parameter scales': to plot the istribution of the elevation 
# for different volume parameter scales
ElevationMode = 'along each link'

# ------------------------------- PROCESS -------------------------------------
# We transform to matfile the links *.txt file.
if saveMat:
    pp.makeFolder(postProcessPath, "matfiles")
    pp.savemat_links(postProcessPath)

if saveGraphs:
    pp.makeFolder(postProcessPath, "graphs")

# List of matfiles inside matfilesPath directory
files = pp.list_matfiles(matfilesPath)

files = sorted(files)  # Sort by name

# For each DEM file we apply the processes defined above
for file in files:

    print("***** Beginning postproces for file: " + file)
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
            plotDeltavsLength,
            plotNodeCount,
            getMatrices,
            saveGraphs,
            directedGraphs,
            Delta,
            plotTotalLength,
            smoothChannels,
            smoothWindow,
        )

        count_nodes.append(count_nodesi)
        coords_nodes.append(coords_nodesi)
        delta_nodes.append(Delta)
        file_names.append(file)
        network_length.append(net_length)
        ordered_nodes.append(ordered_nodesi)
        edges.append(edgesi)
        extremeNodes.append(extremeNodesi)

    if plotDeltavsLength:
        pp.plot_deltavslength(links_original, postProcessPath, file)

if plotNodeCount:
    print("***** Print the number of nodes in time *****")
    pp.plot_nodesEvolution(file_names, delta_nodes, count_nodes, postProcessPath)

if plotTotalLength:
    print("***** Print the network length evolution *****")
    pp.plot_NetworkTotalLength(file_names, delta_nodes, network_length, postProcessPath)

if computeBraidingIndex:
    print("***** Braiding index computation and store in Matfile *****")
    binaryFolder = join(postProcessPath, "binary")
    files = pp.list_png(binaryFolder)

    files = sorted(files)  # Sort by name
    BImatrix = []
    # For each DEM file we apply the processes defined above
    for file in files:
        # print(file)
        binaryFile = join(binaryFolder, file)
        BIvalue = pp.computeBI(binaryFile, choice, columns_selected)
        BImatrix.append([file, BIvalue])

if DEMtimeAverage:
    DEMsPath = join(postProcessPath, "..", "binary")
    DEMavg = pp.time_average(DEMsPath, dt, delta_T, w, h)

if DEMensembleAverage:
    DEMsPath = join(postProcessPath, "..", "binary")
    DEMensAvg = pp.ensemble_average(DEMsPath, w, h)
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    