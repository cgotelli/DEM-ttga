# -------------------------------- IMPORT -------------------------------------
import postprocess_functions as pp

# ------------------------------ PARAMETERS -----------------------------------
# Path for 
pathLinkFiles = '/home/cgotelli/Documents/ttga_DEM/output/'
pathSaveMat = '/home/cgotelli/Documents/ttga_DEM/output/matfiles/'

matfilePath = "/home/cgotelli/Documents/ttga_DEM/output/matfiles/links01_postprocess.mat"
DEM_imagePath = "/home/cgotelli/Documents/ttga_DEM/toProcess/rescaled_dsm02.png"
postProcessPath = "/home/cgotelli/Documents/ttga_DEM/output/"

Delta = 1

# ------------------------------- BOOLEANS ------------------------------------
saveMat = False
plotNetwork = False
printBinary = True

# ------------------------------- PROCESS -------------------------------------
pp.savemat_links(postProcessPath)

links, x_links, y_links = pp.load_matfile(postProcessPath, Delta)
background, w, h, c = pp.load_background(DEM_imagePath)
name = "test" # This should come from the for-loop for each file to postprocess
binary = pp.make_binary(w, h, x_links, y_links, printBinary, 
                        postProcessPath, name)



# pp.postprocess()

