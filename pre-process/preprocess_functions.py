# IMPORT ----------------------------------------------------------------------

import rasterio
from rasterio.enums import Resampling
import numpy as np
import matplotlib.pyplot as plt
from os import listdir, mkdir
from os.path import isfile, join, exists

# FUNCTIONS -------------------------------------------------------------------
def rescaleDEM(DEM, scaleFactor):
    with DEM as dataset:
        # resample data to target shape
        data = dataset.read(
            out_shape=(
                dataset.count,
                int(dataset.height * scaleFactor),
                int(dataset.width * scaleFactor),
            ),
            resampling=Resampling.bilinear,
        )

    return np.squeeze(data)


def printDEM(im_data, dpi, name):
    minValue = np.nanmin(im_data)
    maxValue = np.nanmax(im_data[im_data != np.nanmax(im_data)])

    height, width = np.shape(np.squeeze(im_data))
    figsize = width / float(dpi), height / float(dpi)

    fig = plt.figure(figsize=figsize)
    ax = fig.add_axes([0, 0, 1, 1])

    # Hide spines, ticks, etc.
    ax.axis("off")

    # Display the image.
    ax.imshow(
        im_data,
        vmin=minValue,
        vmax=maxValue,
        interpolation="nearest",
        cmap="Greys_r",
    )

    fig.savefig(name, dpi=dpi, transparent=True)
    plt.show()


def writeFileTTGA(DEM, rows, columns, yres, xres, name):
    minValue = np.nanmin(DEM)
    maxValue = np.nanmax(DEM[DEM != np.nanmax(DEM)])

    with open(name, "w") as f:
        f.write(
            str(rows)
            + " "
            + str(columns)
            + " "
            + str(yres)
            + " "
            + str(xres)
            + " "
            + str(minValue)
            + " "
            + str(maxValue)
            + "\n"
        )
        for line in DEM:
            np.savetxt(f, line, fmt="%.7f")


def detrendDEM(DEM):
    print("detrended")
    DEM = np.squeeze(DEM)
    DEMmean = np.squeeze(np.nanmean(DEM, axis=0))
    print(np.shape(DEM))
    # print(DEMmean)
    plt.plot(
        np.expand_dims(range(0, np.shape(DEM)[1], 1), axis=0).T, DEMmean.T
    )
    plt.show()

    onesMatrix = np.ones_like(DEM)
    DEMmean = np.multiply(DEMmean, onesMatrix)

    DEM = DEM - DEMmean

    return DEM


def DEM_preparation(
    originalDEMsPath,
    detrend,
    toProcessPath,
    orig,
    originalRes,
    resolutionFactor,
    modelFactor,
    dpi,
):

    finalRes = originalRes * modelFactor / resolutionFactor

    for file in listdir(originalDEMsPath):

        if file.endswith(".tif"):
            originalName = join(originalDEMsPath, file)

            src = rasterio.open(originalName)

            if orig:
                originalDEM = src.read()
                originalDEM = np.squeeze(originalDEM)
                originalDEM = np.matrix(originalDEM)
                originalDEM = originalDEM * modelFactor
                columns, rows = np.shape(originalDEM)

                outputName = toProcessPath + "original_" + file[:-4] + ".txt"
                writeFileTTGA(
                    originalDEM, rows, columns, finalRes, finalRes, outputName
                )

            rescaledDEM = rescaleDEM(src, resolutionFactor)
            rescaledDEM[rescaledDEM == -32767] = np.float32("nan")
            rescaledDEM = np.matrix(np.squeeze(rescaledDEM))
            DEM = rescaledDEM * modelFactor
            columns, rows = np.shape(rescaledDEM)

            outputName = toProcessPath + "rescaled_" + file[:-4] + ".txt"
            writeFileTTGA(
                rescaledDEM, rows, columns, finalRes, finalRes, outputName
            )

            outputName = toProcessPath + "rescaled_" + file[:-4] + ".png"
            printDEM(rescaledDEM, dpi, outputName)

            if detrend:
                print("subtracting mean value for file: " + file)
                DEM = detrendDEM(rescaledDEM)
                outputName = toProcessPath + "detrended_" + file[:-4] + ".txt"
                writeFileTTGA(
                    DEM, rows, columns, finalRes, finalRes, outputName
                )

                outputName = toProcessPath + "detrended_" + file[:-4] + ".png"
                printDEM(DEM, dpi, outputName)

    return DEM

def writeBash(
    toProcessPath,
    ttga_path,
    algorithm,
    delta,
    Delta_list,
    simplify,
    hybridStriation,
    xRES,
    xRes,
    yRES,
    yRes,
    minHEIGHT,
    minHeight,
    maxHEIGHT,
    maxHeight,
    ipe,
    links,
    boundary,
    boundary_file_path,
):

    output_path = join(toProcessPath, "../output/links_original")

    if not exists(output_path):
        mkdir(output_path)

    input_DEMs = [
        f
        for f in listdir(toProcessPath)
        if isfile(join(toProcessPath, f)) and f.endswith(".txt")
    ]

    with open(join(toProcessPath, "bashProcess.sh"), "w") as rsh:
        rsh.write("#! /bin/bash \n")

        for DEM in reversed(input_DEMs):

            # Writting the TTGA path
            rsh.write(ttga_path + " ")

            # Writting the options
            if algorithm == False:
                rsh.write("--a persistence" + " ")

            if delta == False:
                rsh.write("-d" + " " + Delta_list + " ")

            if simplify == False:
                rsh.write("-s" + " ")

            if hybridStriation == False:
                rsh.write("--hybridStriation" + " ")

            if xRES == False:
                rsh.write("--xRes" + " " + str(xRes) + " ")

            if yRES == False:
                rsh.write("--xRes" + " " + str(yRes) + " ")

            if minHEIGHT == False:
                rsh.write("--xRes" + " " + str(minHeight) + " ")

            if maxHEIGHT == False:
                rsh.write("--xRes" + " " + str(maxHeight) + " ")

            if ipe == False:
                rsh.write("--ipe" + " ")

            if links == False:
                rsh.write("--links" + " ")

            if boundary == False:
                rsh.write("--boundary" + " " + boundary_file_path + " ")

            # Writting the input path
            rsh.write(toProcessPath + DEM + " ")

            # Writting the input path
            name_DEM = "".join(x for x in DEM[:-4] if x not in ".")
            rsh.write(join(output_path, str(name_DEM)))
            rsh.write("\n")