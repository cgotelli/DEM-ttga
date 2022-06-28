# -------------------------------- IMPORT -------------------------------------
from scipy.io import savemat, loadmat

from os import listdir, mkdir
from os.path import isfile, join, exists

import numpy as np
from math import dist

import matplotlib.pyplot as plt
import networkx as nx

from PIL import Image, ImageOps
import cv2

dpi = 300

# ------------------------------ FUNCTIONS ------------------------------------
def savemat_links(postProcessPath):

    link_sequence_path = join(postProcessPath, "links_original")
    print(
        "Converting links inside this directory to matfile: "
        + link_sequence_path
    )
    # List all the link sequences in the path indicated
    files = [
        f
        for f in listdir(link_sequence_path)
        if isfile(join(link_sequence_path, f)) and f.endswith(".txt")
    ]

    # For all link sequences in the list
    for link_sequence in reversed(files):
        # print(link_sequence)
        # Read of the first line which contains the number of links
        seq = open(link_sequence_path + "/" + link_sequence, "r")
        number_links = seq.readline()
        print("number of links: " + str(number_links))
        # Creation of the link matrix
        link = np.zeros([0, 4])

        # For all links, we want to have a list of the strings of each line
        for line in seq:
            add_list = ""  # string to add in the list
            list_line = []  # list of the strings of the line

            # For each character of the line :
            # if this one is not a delimiter space, we add it in add_list
            # else, we append the string 'add_list' in the list_line
            for i in range(len(line)):
                if line[i] != " ":
                    add_list = add_list + str(line[i])
                else:
                    list_line.append(add_list)
                    add_list = ""
                if i == len(line) - 1:
                    list_line.append(add_list)

            # Define the index link and the delta related to the link
            index_link = list_line[0]
            delta_link = list_line[1]

            # Fill the link matrix
            k = 2
            while k < len(list_line):
                row = np.zeros(4)
                row[0] = index_link
                row[1] = delta_link
                row[2] = list_line[k]
                row[3] = list_line[k + 1]
                link = np.append(link, [row], axis=0)
                k = k + 2

        # Save in a .mat file
        save_path = join(postProcessPath, "matfiles")
        savemat(
            join(save_path, str(link_sequence[:-4] + ".mat")), {"links": link}
        )


def load_matfile(matfilesPath, name, Delta):
    """Reads matfiles and filters according to delta threshold.

    - Input: Path to matfiles, name of matfile, delta value for threshold
    - Returns: links (original and filtered) and coordinates

    Links array format: [link ID, delta Value, x-coord, y-coord]. Each row is
    a point of a link.
    """
    matfilePath = join(matfilesPath, name)
    links = loadmat(matfilePath)
    links_original = links["links"]

    links_filtered = links_original[links_original[:, 1] >= Delta]

    x_links = links_filtered[:, 2]
    y_links = links_filtered[:, 3]
    return links_original, links_filtered, x_links, y_links


def load_background(postProcessPath, name):
    # DEM path should be pointing to the png image made with the preprocess function
    DEMpath = join(postProcessPath, "..", "toProcess", str(name[:-4] + ".png"))
    DEM = plt.imread(DEMpath)
    (h, w, c) = np.shape(DEM)
    return DEM, DEMpath, w, h, c


def makeFolder(postProcessPath, process):
    output_path = join(postProcessPath, process)
    if not exists(output_path):
        mkdir(output_path)


def make_binary(w, h, x_links, y_links, postProcessPath, name, Delta):

    binaryPath = join(postProcessPath, "binary")
    binary = np.zeros((h, w))

    for x, y in zip(x_links, y_links):
        binary[int(y - 1), int(x - 1)] = 1

    height, width = np.shape(np.squeeze(binary))
    figsize = width / float(dpi), height / float(dpi)

    fig = plt.figure(figsize=figsize)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis("off")
    ax.imshow(binary, cmap="Greys_r")

    saveBinaryPath = join(
        binaryPath,
        str(
            name[:-4] + "_Delta" + str("{:1.2f}".format(Delta)) + "_binary.png"
        ),
    )
    # fig.savefig(
    #     saveBinaryPath, dpi=dpi, transparent=False, bbox_inches="tight"
    plt.imsave(saveBinaryPath,binary)
    
    plt.show()

    return binary


def get_nodes(links_filtered, w, h):

    nodes_coords = []

    # Separate link matrix
    index_link = links_filtered[:, 0]

    linksxcoords = links_filtered[:, 2]
    linksycoords = links_filtered[:, 3]

    LinkCount = int(np.max(index_link) + 1)

    for i in range(0, LinkCount):
        # Obtain extremes
        # start point
        firstPointx = linksxcoords[index_link == i][0]
        if firstPointx == -1 or firstPointx == w:
            firstPointx = linksxcoords[index_link == i][1]
            firstPointy = linksycoords[index_link == i][1]
        else:
            firstPointy = linksycoords[index_link == i][0]

        nodes_coords.append([firstPointx, firstPointy])

        # end point
        finalPointx = linksxcoords[index_link == i][-1]

        if finalPointx == -1 or finalPointx == w:
            finalPointx = linksxcoords[index_link == i][-2]
            finalPointy = linksycoords[index_link == i][-2]
        else:
            finalPointy = linksycoords[index_link == i][-1]

        nodes_coords.append([finalPointx, finalPointy])

    nodes_coords = np.unique(nodes_coords, axis=0)
    count_nodes = int(len(nodes_coords))

    return count_nodes, nodes_coords


def plot_network(
    DEMPath,
    postProcessPath,
    links_original,
    links_filtered,
    name,
    Delta,
    includeNodes,
    w,
    h,
):
    # Sonke, 2022.

    saveImgPath = join(postProcessPath, "..", "output", "network")

    img = cv2.imread(DEMPath)

    # Extract each column of the links matrix :
    index_link = links_original[:, 0]
    delta_link = links_original[:, 1]
    x = links_original[:, 2]
    y = links_original[:, 3]

    # Create two arrays that will be used to plot each link :
    X = []
    Y = []

    height, width = np.shape(img)[0:2]
    figsize = 2 * width / float(dpi), 2 * height / float(dpi)

    fig = plt.figure(figsize=figsize)
    ax = fig.add_axes([0, 0, 1, 1])

    for i in range(1, len(x)):

        # The same index value indicates the same link. We extract its coordinates :
        if index_link[i] == index_link[i - 1]:
            X.append(x[i])
            Y.append(y[i])

        else:
            # If the index value change, we plot (X,Y) corresponding to the previous link :
            if delta_link[i - 1] > Delta or delta_link[i - 1] == "inf":
                lab = "delta=" + str("{:1.2f}".format(delta_link[i - 1]))
                # lab = "index=" + str(int(index_link[i - 1]))
                ax = plt.subplot(111)
                ax.plot(X[2:-2], Y[2:-2], label=lab, linewidth=0.5)

            # Then we reset X and Y
            X = []
            Y = []
            X.append(x[i])
            Y.append(y[i])

    ax.imshow(img)

    box = ax.get_position()
    ax.set_position(
        [box.x0, box.y0 + box.height * 0.2, box.width, box.height * 0.8]
    )
    ax.legend(
        loc="upper center",
        bbox_to_anchor=(0.5, -0.05),
        fancybox=False,
        shadow=False,
        ncol=4,
        fontsize=5,
    )
    count_nodes, nodes_coords = get_nodes(links_filtered, w, h)
    if includeNodes:

        for line in nodes_coords:
            plt.scatter(line[0], line[:][1], color="red", s=5)
            plt.title(
                "networks "
                + r"$\delta_{lim}=$"
                + " "
                + str("{:1.2f}".format(Delta))
                + "  &   nodes = "
                + str(count_nodes),
                fontsize=5,
            )
    else:
        fig.suptitle(
            "networks "
            + r"$\delta_{lim}=$"
            + " "
            + str("{:1.1f}".format(Delta)),
            fontsize=5,
        )
    plt.axis("off")

    plt.show()

    saveNetworkPath = join(
        saveImgPath,
        str(
            name[:-4]
            + "_Delta"
            + str("{:1.2f}".format(Delta))
            + "_network.png"
        ),
    )

    fig.savefig(
        saveNetworkPath, dpi=dpi, transparent=False, bbox_inches="tight"
    )


def list_matfiles(matfilesPath):
    files = [
        f
        for f in listdir(matfilesPath)
        if isfile(join(matfilesPath, f)) and f.endswith(".mat")
    ]
    return reversed(files)

def list_png(matfilesPath):
    files = [
        f
        for f in listdir(matfilesPath)
        if isfile(join(matfilesPath, f)) and f.endswith(".png")
    ]
    return reversed(files)

def link_length(x, y):
    length = 0
    for i in range(1, len(x)):
        length += np.sqrt((x[i] - x[i - 1]) ** 2 + (y[i] - y[i - 1]) ** 2)
    return length


def network_length(links, Delta):
    index_link = links[:, 0]
    delta_link = links[:, 1]
    x = links[:, 2]
    y = links[:, 3]
    X = []
    Y = []
    length = 0
    d = 0
    while delta_link[d] >= Delta or delta_link[d] == "inf":
        d += 1
    for i in range(1, d + 1):
        if index_link[i] == index_link[i - 1]:
            X.append(x[i])
            Y.append(y[i])
        else:
            length += link_length(X, Y)
            X = []
            Y = []
            X.append(x[i])
            Y.append(y[i])
    return length


def plot_deltavslength(links, postProcessPath, file):
    # Sonke, 2022.
    delta_link = links[:, 1]
    delta = []
    length = []
    for i in range(1, len(delta_link)):
        if delta_link[i] != delta_link[i - 1] and delta_link[i] > 0.00005:
            delta.append(delta_link[i - 1])
            length.append(network_length(links, delta_link[i - 1]))

    fig = plt.figure()
    plt.plot(delta, length)
    plt.xscale("log")
    plt.yscale("log")
    plt.title("Network length")
    plt.xlabel(r"$\delta$")
    plt.ylabel("Network length")
    plt.axis("on")

    plt.show

    saveImgPath = join(postProcessPath, "..", "output", "others")

    saveVolumePath = join(
        saveImgPath,
        str(file[:-4] + "_volumeLength.png"),
    )

    fig.savefig(saveVolumePath, dpi=dpi, transparent=False, box_inches="tight")


def plot_NetworkTotalLength(
    file_names, delta_nodes, network_length, postProcessPath
):
    # Sonke, 2022.
    fig = plt.figure(figsize=(8, 6))
    plt.style.use("seaborn-white")
    # For each delta value,  we plot the network lenght for all DEMs
    deltas = np.unique(delta_nodes)

    for value in deltas:
        xToPlot = []
        yToPlot = []
        for i in range(0, len(delta_nodes)):
            if delta_nodes[i] == value:
                xToPlot.append(file_names[i][:-4])
                yToPlot.append(network_length[i])
        plt.plot(
            xToPlot,
            yToPlot,
            ".-",
            markersize=12,
            label="delta=" + str("{:1.2f}".format(delta_nodes[i])),
        )

    plt.ylabel("Network length")
    plt.xlabel("DEM files")
    plt.xticks(rotation=45)
    plt.axis("on")
    plt.show
    plt.tight_layout()

    saveImgPath = join(postProcessPath, "..", "output", "others")
    saveVolumePath = join(
        saveImgPath,
        str("NetworkTotalLength.png"),
    )

    fig.savefig(saveVolumePath, transparent=False, box_inches="tight")


def plot_nodesEvolution(file_names, delta_nodes, count_nodes, postProcessPath):
    # Sonke, 2022.

    fig = plt.figure(figsize=(8, 6))
    plt.style.use("seaborn-white")
    # For each delta value,  we plot the network lenght for all DEMs
    deltas = np.unique(delta_nodes)

    for value in deltas:
        xToPlot = []
        yToPlot = []

        for i in range(0, len(delta_nodes)):
            if delta_nodes[i] == value:
                xToPlot.append(file_names[i][:-4])
                yToPlot.append(count_nodes[i])
        plt.plot(
            xToPlot,
            yToPlot,
            ".-",
            markersize=12,
            label="delta=" + str("{:1.2f}".format(delta_nodes[i])),
        )

    plt.ylabel("Nodes count")
    plt.xlabel("DEM files")
    plt.axis("on")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show

    saveImgPath = join(postProcessPath, "..", "output", "others")
    saveVolumePath = join(
        saveImgPath,
        str("NodesCount.png"),
    )

    fig.savefig(saveVolumePath, transparent=False, bbox_inches="tight")


def postprocess(
    postProcessPath,
    matfilesPath,
    file,
    matfile,
    network,
    binary,
    includeNodes,
    compute_length,
    plotDeltavsLength,
    plotNodeCount,
    getMatrices,
    saveGraphs,
    directed,
    Delta,
    totalLength,
    smoothChannels,
    smoothWindow,
):

    count_nodes = []
    coords_nodes = []
    net_length = []
    ordered_nodes = []
    edges = []
    extremeNodes = []

    # Takes files from the Matfiles folder and apply the selected process

    if network:
        makeFolder(postProcessPath, "network")
    if binary:
        makeFolder(postProcessPath, "binary")
    if plotDeltavsLength or plotNodeCount or totalLength:
        makeFolder(postProcessPath, "others")

    print("- Processing with Delta " + str("{:1.2f}".format(Delta)))

    # Load matfile with links details
    links_original, links_filtered, x_links, y_links = load_matfile(
        matfilesPath, file, Delta
    )

    # Load DEM for plots
    DEM, DEMpath, w, h, c = load_background(postProcessPath, file)

    count_nodes, coords_nodes = get_nodes(links_filtered, w, h)
    if network:
        plot_network(
            DEMpath,
            postProcessPath,
            links_original,
            links_filtered,
            file,
            Delta,
            includeNodes,
            w,
            h,
        )

    if smoothChannels:
        x_links, y_links = smooth(links_original, Delta, smoothWindow, w, h)

    if binary:
        make_binary(w, h, x_links, y_links, postProcessPath, file, Delta)

    if compute_length:
        net_length = network_length(links_original, Delta)

    if getMatrices:
        # get edges for function using package networkx
        edges = get_edges(links_filtered, coords_nodes, w, h)
        #
        make_network(coords_nodes, edges, w, h, directed, file, Delta, saveGraphs, postProcessPath)

    return (
        links_original,
        links_filtered,
        count_nodes,
        coords_nodes,
        net_length,
        ordered_nodes,
        edges,
        extremeNodes,
    )


def get_index_positions(list_of_elems, element):
    """Returns the indexes of all occurrences of give element in
    the list- listOfElements"""
    index_pos_list = []
    index_pos = 0
    while True:
        try:
            # Search for item in list from indexPos to the end of list
            index_pos = list_of_elems.index(element, index_pos)
            # Add the index position in list
            index_pos_list.append(index_pos)
            index_pos += 1
        except ValueError as e:
            break
    return index_pos_list


def get_edges(links_filtered, coords_nodes, w, h):
    edges = []

    # Separate link matrix
    index_link = links_filtered[:, 0]

    linksxcoords = links_filtered[:, 2]
    linksycoords = links_filtered[:, 3]

    nodesxcoords = np.array(coords_nodes)[:, 0]
    nodesycoords = np.array(coords_nodes)[:, 1]

    LinkCount = int(np.max(index_link) + 1)

    for i in range(0, LinkCount):
        edge = []
        linkxpoints = linksxcoords[index_link == i]
        linkypoints = linksycoords[index_link == i]

        for j in range(0, len(linkxpoints)):

            xpoint = linkxpoints[j]
            ypoint = linkypoints[j]

            xindex = get_index_positions(list(nodesxcoords), xpoint)
            yindex = get_index_positions(list(nodesycoords), ypoint)

            intersect = list(set(xindex).intersection(yindex))
            # print(intersect)
            if len(intersect) != 0:  # If the point is a node
                if len(edge) == 0:
                    edge.append(intersect)

                elif len(edge) == 1:
                    edge = np.squeeze(np.array([edge[0], intersect]))

                    edges.append(edge)

                    edge = [intersect]

    return edges


def make_network(coords_nodes, edges, w, h, directed, name, Delta, saveGraphs, postProcessPath):
    
    if directed:
        G = nx.DiGraph()
    else:
        G = nx.Graph()

    for i in range(0, len(coords_nodes)):
        G.add_node(i, pos=(coords_nodes[i][0], h - coords_nodes[i][1]))

    pos = nx.get_node_attributes(G, "pos")

    if len(pos) > 2:
        G.add_edges_from(edges)
    else:
        G.add_edge(edges[0][0], edges[0][1])

    fig = plt.figure()
    nx.draw(G, pos, with_labels=True)
    plt.axis("off")
    plt.xlim([-50, w + 50])
    
    plt.ylim([-50, h + 50])
    plt.show()

    if saveGraphs:
        saveGraphPath = join(
            postProcessPath,'graphs',
            str(
                name[:-4]
                + "_Delta"
                + str("{:1.2f}".format(Delta))
                + "_graph.png"
            ),
        )
        fig.savefig(
            saveGraphPath, dpi=dpi, transparent=False, bbox_inches="tight"
        )

    return


def find_nearest(direction, point, links, w, h):

    # for each direction, we take the coordinate that will change depending on
    # the direction and we add to it +/- 1. As long as the new coordinate does
    # not include in the links, we continue. The function returns the coordinate
    # of the nearest point once we reach a link, except if we reach the boundary.

    # the file links containing the links is the file .mat
    # w and h are respectively the width and the height of the DEM

    if (
        direction == "nord" and int(point[1]) < h
    ):  # check if the point is not out of the boundaries
        y = int(point[1]) + 1  # +1 to go the the north
        while [
            int(point[0]),
            y,
        ] not in links.tolist():  # while the new point is not on a link
            if y < h:  # check if the new point is not out of the boundaries
                y += 1
            else:
                return "Boundary reached : no nearest value"
        return int(point[0]), y  # return the point once we reach a link

    # repeat the same for the other 3 directions
    if direction == "sud" and point[1] > 0:
        y = int(point[1]) - 1
        while [int(point[0]), y] not in links.tolist():
            if y > 0:
                y = y - 1
            else:
                return "Boundary reached : no nearest value"
        return int(point[0]), y

    if direction == "est" and point[0] < w:
        x = int(point[0]) + 1
        while [x, int(point[1])] not in links.tolist():
            if x < w:
                x += 1
            else:
                return "Boundary reached : no nearest value"
        return x, int(point[1])

    if direction == "ouest" and point[0] > 0:
        x = int(point[0]) - 1
        while [x, int(point[1])] not in links.tolist():
            if x > 0:
                x = x - 1
            else:
                return "Boundary reached : no nearest value"
        return x, int(point[1])

    else:
        return "Boundary reached : no nearest value"


def close_gap(point, link, links, w, h):
    
    # close_gap return a matrix which contains the coordinates of the points
    # used to close the gap between a point and its nearest point in an other link

    # the file links is the file .mat
    # w and h are respectively the width and the height of the DEM

    link_gap = np.zeros((0, 2))

    # direction nord

    if (
        find_nearest("nord", point, links, w, h)
        != "Boundary reached : no nearest value"
    ):
        # check that the nearest point is not out of the boundaries
        x_nord, y_nord = find_nearest(
            "nord", point, links, w, h
        )  # take the coordinates of the nearest point
        # check if the nearest point is not in the link
        while [
            x_nord,
            y_nord,
        ] in link.tolist():  # if the nearest point is in the link
            if (
                find_nearest("nord", [x_nord, y_nord], links, w, h)
                != "Boundary reached : no nearest value"
            ):
                # we continue the search of the nearest point, starting from the previous nearest point
                x_nord, y_nord = find_nearest(
                    "nord", [x_nord, y_nord], links, w, h
                )
            else:
                break
        # if the nearest point is not in the link, we compute the distance between the point and the nearest point
        dist_nord = dist(point, [x_nord, y_nord])
    else:  # if we reach the boundary, the distance between the point and the
        # nearest point contained in the links does not exist (unknown)
        dist_nord = "unknowm"

    # repeat the same for the other 3 directions

    # direction est
    if (
        find_nearest("est", point, links, w, h)
        != "Boundary reached : no nearest value"
    ):
        x_est, y_est = find_nearest("est", point, links, w, h)
        while [x_est, y_est] in link.tolist():
            if (
                find_nearest("est", [x_est, y_est], links, w, h)
                != "Boundary reached : no nearest value"
            ):
                x_est, y_est = find_nearest("est", [x_est, y_est], links, w, h)
            else:
                break
        dist_est = dist(point, [x_est, y_est])
    else:
        dist_est = "unknowm"

    # direction sud
    if (
        find_nearest("sud", point, links, w, h)
        != "Boundary reached : no nearest value"
    ):
        x_sud, y_sud = find_nearest("sud", point, links, w, h)
        while [x_sud, y_sud] in link.tolist():
            if (
                find_nearest("sud", [x_sud, y_sud], links, w, h)
                != "Boundary reached : no nearest value"
            ):
                x_sud, y_sud = find_nearest("sud", [x_sud, y_sud], links, w, h)
            else:
                break
        dist_sud = dist(point, [x_sud, y_sud])
    else:
        dist_sud = "unknowm"

    # direction ouest
    if (
        find_nearest("ouest", point, links, w, h)
        != "Boundary reached : no nearest value"
    ):
        x_ouest, y_ouest = find_nearest("ouest", point, links, w, h)
        while [x_ouest, y_ouest] in link.tolist():
            if (
                find_nearest("ouest", [x_ouest, y_ouest], links, w, h)
                != "Boundary reached : no nearest value"
            ):
                x_ouest, y_ouest = find_nearest(
                    "ouest", [x_ouest, y_ouest], links, w, h
                )
            else:
                break
        dist_ouest = dist(point, [x_ouest, y_ouest])
    else:
        dist_ouest = "unknowm"

    # create a list with all the distances computed in several directions
    l = [
        x
        for x in [dist_nord, dist_est, dist_sud, dist_ouest]
        if x != "unknowm"
    ]

    if l != []:  # if the list is not empty, we compute the minimum distance
        min_dist = min(l)

        if min_dist == dist_nord:
            # we fill the gap between the point and the nearest point by filling the matrix link_gap
            for i in range(0, y_nord - int(point[1])):
                link_gap = np.append(
                    link_gap, np.array([[point[0], int(point[1]) + i]]), axis=0
                )
        if min_dist == dist_est:
            for i in range(0, x_est - int(point[0])):
                link_gap = np.append(
                    link_gap, np.array([[int(point[0]) + i, point[1]]]), axis=0
                )
        if min_dist == dist_sud:
            for i in range(0, int(point[1]) - y_sud):
                link_gap = np.append(
                    link_gap, np.array([[point[0], int(point[1]) - i]]), axis=0
                )
        if min_dist == dist_ouest:
            for i in range(0, int(point[0]) - x_ouest):
                link_gap = np.append(
                    link_gap, np.array([[int(point[0]) - i, point[1]]]), axis=0
                )

    return link_gap


def smooth(links_original, Delta, window, w, h):

    # Function used to smooth the links for a threshold value.
    # A high threshold value will imply a high smoothing
    # Return the coordinates x and y of the smoothed links

    # the file links is the file .mat
    # w and h are respectively the width and the height of the DEM

    # data = loadmat(links)
    # links = data['links']
    index_link = links_original[:, 0]
    delta_link = links_original[:, 1]
    x = links_original[:, 2]
    y = links_original[:, 3]
    d = 0

    # taking all the indexes > delta
    while delta_link[d] >= Delta or delta_link[d] == "inf":
        d += 1

    # indexes is a list of lists containing the index lists of each link
    indexes = []
    index_list = []
    for i in range(1, d + 1):
        if index_link[i] == index_link[i - 1]:
            index_list.append(i)
        else:
            indexes.append(index_list)
            index_list = []
            index_list.append(i)

    # create a matrix which will store the coordinates of the smooth links
    Smooth = np.zeros([0, 2])

    for index in indexes:  # for all index list
        i = index[0]  # the first point index of the link
        Smooth_x = []
        Smooth_y = []
        # compute the moving average for the link
        while i < index[-1] - window + 1:
            x_average = sum(x[i : i + window]) / window
            y_average = sum(y[i : i + window]) / window
            Smooth_x.append(int(x_average))
            Smooth_y.append(int(y_average))
            i = i + 1

        # fill the missing values
        missing_values = window - 1
        link1_x = [x for x in x[index[0] : index[-1] + 1]]
        link1_y = [y for y in y[index[0] : index[-1] + 1]]
        link2_x = [x for x in Smooth_x[:]]
        link2_y = [x for x in Smooth_y[:]]
        link3 = np.zeros([len(index), 2])

        if window % 2 == 0:
            index_to_complete = int(missing_values / 2) + 1
        else:
            index_to_complete = int(missing_values / 2) + 1

        for i in range(0, len(link2_x)):
            link3[i + index_to_complete][0] = link2_x[i]
            link3[i + index_to_complete][1] = link2_y[i]

        for i in range(0, index_to_complete):
            link3[i][0] = link1_x[i]
            link3[i][1] = link1_y[i]
            link3[len(index) - i - 1][0] = link1_x[len(link1_x) - i - 1]
            link3[len(index) - i - 1][1] = link1_y[len(link1_y) - i - 1]

        Smooth = np.append(Smooth, link3, axis=0)

    Smooth2 = Smooth

    # fill the gap
    for index in indexes:  # for each index of each link
        # store the coordinates of each point of each link
        link_x = [x for x in Smooth2[index[0] - 1 : index[-1], 0]]
        link_y = [y for y in Smooth2[index[0] - 1 : index[-1], 1]]
        # take the coordinates of the first point and the last point of the link
        point0 = [link_x[0], link_y[0]]
        point1 = [link_x[-1], link_y[-1]]

        # fill the gap between the first and the last points and their nearest points
        if 0 < point0[0] < w and 0 < point0[1] < h:
            link_gap0 = close_gap(
                point0, np.transpose(np.array([link_x, link_y])), Smooth2, w, h
            )
            Smooth = np.append(Smooth, link_gap0, axis=0)
        if 0 < point1[0] < w and 0 < point1[1] < h:
            link_gap1 = close_gap(
                point1, np.transpose(np.array([link_x, link_y])), Smooth2, w, h
            )
            Smooth = np.append(Smooth, link_gap1, axis=0)
            # in the smooth matrix which contains the smooth links, we add the gap coordinates

    return ([row[0] for row in Smooth], [row[1] for row in Smooth])


def computeBI(binary, choice, column_selected):
    
    # Compute the number of branches for different sections
    # The sections can be chosen in 'column_selected' --> choice = 'selected'
    # otherwise, all the sections are computed --> choice = 'all'

    # binary is the binary path

    img = Image.open(binary)
    img = ImageOps.grayscale(img)
    img = np.array(img.convert("L"))
    img[img == 0] = 1
    height, width = np.shape(img)
    
    plt.imshow(img, cmap="Greys")

    if choice == "selected":
        for index in column_selected:
            if index > width:
                print("Column index ", index, " is out of image width")
                return None

        nbranches = np.zeros([0, 2])
        for j in column_selected:
            count_branches = 0
            for i in range(0, height):
                if img[i][j] == 1:
                    count_branches += 1
            nbranches = np.append(nbranches, [[j, count_branches]], axis=0)
        # print(nbranches)
        return nbranches

    elif choice == "all":
        nbranches = np.zeros([0, 2])
        for j in range(0, width):
            count_branches = 0
            for i in range(0, height):
                if img[i][j] == 1:
                    count_branches += 1
            nbranches = np.append(nbranches, [[j, count_branches]], axis=0)
        # print(nbranches)
        return nbranches

    # return a matrix containing the sections and number of branches related
