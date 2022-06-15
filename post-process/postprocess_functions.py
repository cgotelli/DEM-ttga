# -------------------------------- IMPORT -------------------------------------
from scipy.io import savemat, loadmat
from os import listdir, mkdir
from os.path import isfile, join, exists
import numpy as np
import matplotlib.pyplot as plt
import cv2

dpi = 10


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
        print(link_sequence)
        # Read of the first line which contains the number of links
        seq = open(link_sequence_path + "/" + link_sequence, "r")
        number_links = seq.readline()

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
    matfilePath = join(matfilesPath, name)
    links = loadmat(matfilePath)
    links = links["links"]

    links_filtered = links[links[:, 1] >= Delta]

    x_links = links_filtered[:, 2]
    y_links = links_filtered[:, 3]
    return links, x_links, y_links


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
    fig.savefig(saveBinaryPath, dpi=dpi, transparent=True)

    plt.show()

    return binary


def compute_nodes(links, Delta):
    # data = loadmat(network)
    # links = data['links']
    index_link = links[:, 0]
    delta_link = links[:, 1]
    x = links[:, 2]
    y = links[:, 3]
    nodes = np.empty([0, 2])
    count_nodes = 0
    d = 0
    while delta_link[d] >= Delta or delta_link[d] == "inf":
        d += 1
    for i in range(0, d):
        if (
            index_link[i] != index_link[i - 1]
            or index_link[i] != index_link[i + 1]
        ):
            nodes = np.append(nodes, np.array([[x[i], y[i]]]), axis=0)
    nodes = np.unique(nodes, axis=0)
    for line in nodes:
        count_nodes += 1
    return count_nodes, nodes


def plot_network(DEMPath, postProcessPath, links, name, Delta, findNodes):
    # Read the .mat file and the DEM :
    # data = loadmat(networks)
    # networks = join(postProcessPath)

    # print(DEMPath)
    saveImgPath = join(postProcessPath, "..", "output", "network")
    # print(saveImgPath)

    img = cv2.imread(DEMPath)

    # Extract each column of the links matrix :
    index_link = links[:, 0]
    delta_link = links[:, 1]
    x = links[:, 2]
    y = links[:, 3]

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
                ax = plt.subplot(111)
                ax.plot(X, Y, label=lab, markersize=0.5)

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
        ncol=3,
    )

    if findNodes:
        # print("entered nodes")
        count_nodes, Node = compute_nodes(links, Delta)
        for line in Node:
            plt.scatter(line[0], line[:][1], color="red")
            plt.title(
                "networks "
                + r"$\delta_{lim}=$"
                + " "
                + str("{:1.2f}".format(Delta))
                + "  &   nodes = "
                + str(count_nodes)
            )
    else:
        plt.title(
            "networks "
            + r"$\delta_{lim}=$"
            + " "
            + str("{:1.1f}".format(Delta))
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

    fig.savefig(saveNetworkPath, dpi=dpi, transparent=False)
    return count_nodes, Node


def list_matfiles(matfilesPath):
    files = [
        f
        for f in listdir(matfilesPath)
        if isfile(join(matfilesPath, f)) and f.endswith(".mat")
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


def plot_volume_length(links, postProcessPath, file):

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

    fig.savefig(saveVolumePath, dpi=dpi, transparent=False)


def plot_length(file_names, delta_nodes, network_length, postProcessPath):
    fig = plt.figure()
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
    plt.axis("on")
    plt.show

    saveImgPath = join(postProcessPath, "..", "output", "others")
    saveVolumePath = join(
        saveImgPath,
        str("NetworkLength.png"),
    )

    fig.savefig(saveVolumePath, dpi=dpi, transparent=False)


def plot_nodes(file_names, delta_nodes, count_nodes, postProcessPath):

    fig = plt.figure()
    plt.style.use("seaborn-white")
    # For each delta value,  we plot the network lenght for all DEMs
    deltas = np.unique(delta_nodes)

    for value in deltas:
        xToPlot = []
        yToPlot = []
        print(value)
        print(len(delta_nodes))
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
    plt.show

    saveImgPath = join(postProcessPath, "..", "output", "others")
    saveVolumePath = join(
        saveImgPath,
        str("NodesCount.png"),
    )

    fig.savefig(saveVolumePath, dpi=dpi, transparent=False)


def postprocess(
    postProcessPath,
    matfilesPath,
    file,
    matfile,
    network,
    binary,
    findNodes,
    computeLength,
    plotVolume,
    plotNodeCount,
    Delta,
):
    # Takes files from the Matfiles folder and apply the selected process

    # link_sequence_path = join(postProcessPath, "links_original")

    if network:
        makeFolder(postProcessPath, "network")
    if binary:
        makeFolder(postProcessPath, "binary")
    if plotVolume or plotNodeCount:
        makeFolder(postProcessPath, "others")

    print("- Processing with Delta " + str("{:1.2f}".format(Delta)))

    # Load matfile with links details
    links, x_links, y_links = load_matfile(matfilesPath, file, Delta)
    # Load DEM for plots
    DEM, DEMpath, w, h, c = load_background(postProcessPath, file)

    if network:
        # print("execute plot network")
        count_nodes, coords_nodes = plot_network(
            DEMpath, postProcessPath, links, file, Delta, findNodes
        )

    if binary:
        make_binary(w, h, x_links, y_links, postProcessPath, file, Delta)

    if computeLength:
        net_length = network_length(links, Delta)

    # plot_nodes(nodes)

    return links, count_nodes, coords_nodes, net_length
