# -------------------------------- IMPORT -------------------------------------
from os import listdir, mkdir
from os.path import isfile, join, exists

# ------------------------------- BOOLEANS ------------------------------------
# The default mode is defined by 'true'.
# To modify the settings, change 'true' by 'false'.

algorithm = False  # Striation => True
# Persistence => False
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


# ------------------------------ PARAMETERS -----------------------------------
# Enter in input_path the path of the file containing the DEMS to process
# coming from script DEM_preparation-ttga.py
input_path = "/home/cmgotelli/Documents/ttga_DEM/toProcess/"

# Path to executable file of ttga
ttga_path = "/home/cmgotelli/Documents/ttga_software/build/src/gui/ttga"


Delta_list = ""
xRes = 0.1
yRes = 0.1
minHeight = 0
maxHeight = 10
boundary_file_path = ""


# ------------------------------- PROCESS -------------------------------------

output_path = join(input_path, "../output/links_original")

if not exists(output_path):
    mkdir(output_path)

input_DEMs = [
    f for f in listdir(input_path) if isfile(join(input_path, f)) and f.endswith(".txt")
]

with open(join(input_path, "bashProcess.sh"), "w") as rsh:
    rsh.write("#! /bin/bash \n")

    for DEM in input_DEMs:

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
        rsh.write(input_path + DEM + " ")

        # Writting the input path
        name_DEM = "".join(x for x in DEM[:-4] if x not in ".")
        rsh.write(join(output_path, str(name_DEM)))
        rsh.write("\n")
