import DEM_functions_ttga as DF

# PATHS -----------------------------------------------------------------------
originalDEMsPath = "/home/cgotelli/Documents/ttga_DEM/originalDEMs/"
toProcessPath = originalDEMsPath + "/../toProcess/"

# PARAMETERS ------------------------------------------------------------------
originalRes = 0.0004  # Meters per pixel in DEM from Metashape
resolutionFactor = 1 / 10  # Factor to increase/decrease DEM resolution
modelFactor = 30  # Scale between model and prototype
dpi = 900
orig = False  # Converts or not the original resolution to txt
detrend = True  # Remove mean value

# PROCESS ---------------------------------------------------------------------
DEM = DF.Process(
    originalDEMsPath,
    detrend,
    toProcessPath,
    orig,
    originalRes,
    resolutionFactor,
    modelFactor,
    dpi,
)
