# DEM-ttga


This code is for doing the pre- and post-treatment of laboratory-scale DEMs processed with the software **TTGA: Topological Tools for Geomorphological Analysis**. TTGA is a tool for Unix and Windows OS, which helps the analysis of river systems, in particular, braided rivers and estuaries. The focus of the tool is the computation of river networks from a digital elevation model (DEM) of the river bed. The software can be found in his original repository [here](https://github.com/tue-alga/ttga) or in [Zenodo](https://doi.org/10.5281/zenodo.3634684).  

The code is divided in 2 main steps:
- The preprocess for DEM files to get them ready for being processed with TTGA, and the preparation of the bash file for running TTGA from the console for all DEMs automatically one after the other.
- The postprocess of the TTGA output files. Several functions are available for computing different river network parameters (e.g. number of brances, number of nodes, etc.).  

The structure of the code is shown below in a folder tree view.

```
DEM-ttga
├───ttga-software
│       ttga-code.zip
|       ttga-manual.pdf
|   
├───pre-process
│       preprocess_functions.py
│       preprocess.py
│
└───post-process
        postprocess_functions.py
        postprocess.py
```

Inside the main folder of the repository we find three subfolders. The first contains the source code for the version of the software for which this code was developed and has been tested to work. The other two subfolders contain the scripts with all the used functions for each process. Depending on the process, the only files to be modified are ```DEM_preparation-ttga.py``` or ```postprocess.py```.


## Using the code

For using the code it is only necessary to have the all the original DEM files to process inside the same folder (in ```*.tif``` format), and to set a few parameters for the different steps. In this section we just explain the general steps for the entire process, whilst a more detailed explanation is given in the README file inside each process subfolder.  

The general steps are as follows:

1. Assuming we have TTGA (already compiled) and all the other required files in the directory ```/home/user/Documents/networkAnalysis/```, before starting we should have a structure similar to:  

```
home/user/Documents/networkAnalysis/
├───ttga-software
│       ├── build
│       ├── cmake
│       ├── doc-images
│       ├── manual
│       └── src
│       
├───files
│       └── originalDEMs
│   
├───pre-process
│       preprocess_functions.py
│       preprocess.py
│
└───post-process
        postprocess_functions.py
        postprocess.py

```
IMPORTANT: Based on the file structure shown above, the executable of TTGA should be in the path: ```/home/user/Documents/networkAnalysis/ttga-software/build/src/gui/ttga```. This path is important for preparing the bash file.

2. By using the script ```DEM_preparation-ttga.py``` it converts ```*.tif``` files into the specific ```*.txt``` formatted file used by TTGA. It requires only the path where the original DEMs are stored. It will put the files to process with TTGA in a new folder called "toProcess". See the folder tree below for further details.
3. The file ```write_Bash-ttga.py```










