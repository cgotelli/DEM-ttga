# IMPORT ----------------------------------------------------------------------
import os
import rasterio
from rasterio.enums import Resampling
import numpy as np
import matplotlib.pyplot as plt

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
        im_data, vmin=minValue, vmax=maxValue, interpolation="nearest", cmap="Greys_r"
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
    plt.plot(np.expand_dims(range(0, np.shape(DEM)[1], 1), axis=0).T, DEMmean.T)
    plt.show()

    onesMatrix = np.ones_like(DEM)
    DEMmean = np.multiply(DEMmean, onesMatrix)

    DEM = DEM - DEMmean

    return DEM


def Process(
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

    for file in os.listdir(originalDEMsPath):

        if file.endswith(".tif"):
            originalName = os.path.join(originalDEMsPath, file)

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
            writeFileTTGA(rescaledDEM, rows, columns, finalRes, finalRes, outputName)

            outputName = toProcessPath + "rescaled_" + file[:-4] + ".png"
            printDEM(rescaledDEM, dpi, outputName)

            if detrend:
                print("subtracting mean value for file: " + file)
                DEM = detrendDEM(rescaledDEM)
                outputName = toProcessPath + "detrended_" + file[:-4] + ".txt"
                writeFileTTGA(DEM, rows, columns, finalRes, finalRes, outputName)

                outputName = toProcessPath + "detrended_" + file[:-4] + ".png"
                printDEM(DEM, dpi, outputName)

    return DEM


# PATHS -----------------------------------------------------------------------
originalDEMsPath = "/home/cmgotelli/Documents/ttga_DEM/originalDEMs/"
toProcessPath = originalDEMsPath + "/../toProcess/"

# PARAMETERS ------------------------------------------------------------------
originalRes = 0.0004  # Meters per pixel in DEM from Metashape
resolutionFactor = 1 / 10  # Factor to increase/decrease DEM resolution
modelFactor = 30  # Scale between model and prototype
dpi = 900
orig = False  # Converts or not the original resolution to txt
detrend = False  # Remove mean value

# PROCESS ---------------------------------------------------------------------
DEM = Process(
    originalDEMsPath,
    detrend,
    toProcessPath,
    orig,
    originalRes,
    resolutionFactor,
    modelFactor,
    dpi,
)
