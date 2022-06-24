import preprocess_functions as df
import os

# --------------------------------- PATHS -------------------------------------
# Path where the original DEMs are stored
originalDEMsPath = "/home/cgotelli/Documents/ttga_DEM/originalDEMs/"
# Path for TTGA's executable file. Read the README file for folder structure example.
ttga_path = "/home/cgotelli/Documents/ttga_software/build/src/gui/ttga"

# ---------------------- DEM preparation parameters ---------------------------
originalRes = 0.0004  # Meters per pixel in original DEMs
resolutionFactor = 1 / 10  # Factor to increase/decrease DEM resolution
modelFactor = (
    30  # Scale between model and prototype. Set 1 for real size DEMs.
)
dpi = 900  # Image quality
orig = False  # Convert or not the original resolution DEM to TTGA-txt input
detrend = True  # Remove mean value

# --------------------------------- TTGA --------------------------------------

# BOOLEANS FOR CHOOSING TTGA'S OPTIONS
# The default mode is defined by 'true'.
# To modify the settings, change 'true' by 'false'.

algorithm = False  # Striation => True Persistence => False
delta = True  # To modify delta => False
simplify = True  # To simplify the output in striation => False
hybridStriation = True  # To use the hybrid striation strategy => False
xRES = True  # To modify xRes => False
yRES = True  # To modify yRes => False
minHEIGHT = True  # To modify minHeight => False
maxHEIGHT = True  # To modify maxHeight => False
ipe = True  # To output an Ipe figure => False
links = False  # To output a link sequence instead of graph => False. Should be always False!
boundary = True  # To specify a river boundary file => False


# PARAMETERS FOR TTGA COMPUTATION

Delta_list = ""
xRes = 0.1
yRes = 0.1
minHeight = 0
maxHeight = 10
boundary_file_path = ""


# --------------------------------- TTGA --------------------------------------

toProcessPath = os.path.join(originalDEMsPath, "..","toProcess/")

DEM = df.DEM_preparation(
    originalDEMsPath,
    detrend,
    toProcessPath,
    orig,
    originalRes,
    resolutionFactor,
    modelFactor,
    dpi,
)

df.writeBash(
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
)
