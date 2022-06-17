# DEM-ttga

This code is for doing the pre- and post-treatment of laboratory-scale DEMs processed with the software **TTGA: Topological Tools for Geomorphological Analysis**. TTGA is a tool for Unix and Windows OS, which helps the analysis of river systems, in particular, braided rivers and estuaries. The focus of the tool is the computation of river networks from a digital elevation model (DEM) of the river bed. The software can be found in his original repository [here](https://github.com/tue-alga/ttga) or in [Zenodo](https://doi.org/10.5281/zenodo.3634684).  

This code is divided in 3 main steps:
- The preprocess of DEM files to get them ready for being processed with TTGA: resolution change and format conversion for being used with TTGA. Also the  preparation of the bash file for running all the DEMs in series from console.
- Running the TTGA process from console.
- The postprocess of TTGA output files. Several functions are available for computing different river network parameters (e.g. number of brances, number of nodes, etc.).  

The structure of the code before running is shown below.

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

Inside the main folder of the repository we find three subfolders. The first contains the source code for the version of the software for which this code was developed and has been tested to work. The other two subfolders contain the scripts with all the used functions for each process. The only files that must be modified are ```DEM_preparation-ttga.py``` and ```postprocess.py```.

## Using the code

For using the code it is only necessary to have inside the same folder all the original DEM files to process (in ```*.tif``` format), and to set a few parameters for the different steps. In this section we just explain the general steps for the entire process, whilst a more detailed explanation is given in the README file inside the subfolder of each process.  

The general steps are as follows:

1. Assuming that before starting we have TTGA (already compiled) and all the other required files in the directory ```/home/user/Documents/networkAnalysis/```,  we should have a structure similar to:  

```
home/user/Documents/networkAnalysis/
├───ttga-software
│       ├── build
│       ├── cmake
│       ├── doc-images
│       ├── manual
│       └── src
│   
├───pre-process
│       preprocess_functions.py
│       preprocess.py
│
├───post-process
│       postprocess_functions.py
│       postprocess.py
│
└───files
        └── originalDEMs
                DEM_file01.tif
                DEM_file02.tif
                DEM_file03.tif
                ...

```
> :warning: **Important**: It is necessary to compile the TTGA's source code inside folder _ttga-software_. Based on the file structure shown above, after compiling, the executable of TTGA should be in the path: ```/home/user/Documents/networkAnalysis/ttga-software/build/src/gui/ttga```. This path is important for preparing the bash file afterwards.

2. The file ```preprocess.py``` is in charge of the complete preprocess. It requires only the path where the original DEMs are stored and the path of the executable ttga file (see the important note above for details). With function **DEM_preparation** it converts the ```*.tif``` DEMs into ```*.txt``` files with the specific format used by TTGA, and stores them in a new folder called _toProcess_ (see below the details of the final folder structure). It also writes a ```*.png``` version of the DEM to be used during the postprocess.

The function also creates the bash file ```bashProcess.sh``` used for running TTGA on all the DEM files previously transformed from ```*.tif``` to ```*.txt```. 

3. The next step is to run TTGA from the Terminal(in UNIX) or Anaconda Prompt (in Windows). For that is necessary to run the code ```sh bashProcess.sh``` in the directory where the bash file was automatically stored. In the example we are using it would be the path ```/home/user/Documents/files/toProcess/```. The output ```*.txt``` files which contain all the detected links for each $\delta$ and each DEM file, are stored in a subfolder inside the folder _output_.

4. The output files with the links are the base for the postprocess. The file ```postprocess.py``` has different functions for postprocessing the network. The detail of these functions can be found in the README file inside the _post-process_ folder.

The final distribution of folders and files is can be found below.


```
home/user/Documents/networkAnalysis/
├───ttga-software
│       ├── build
│       ├── cmake
│       ├── doc-images
│       ├── manual
│       └── src
│       
├───pre-process
│       preprocess_functions.py
│       preprocess.py
│
├───post-process
│       postprocess_functions.py
│       postprocess.py
│        
└───files
        ├── originalDEMs
        │       DEM_file01.tif
        │       DEM_file02.tif
        │       DEM_file03.tif
        │       ...
        │
        ├── toProcess
        │       bashProcess.sh
        │       DEM_file01.png
        │       DEM_file01.txt
        │       DEM_file02.png
        │       DEM_file02.txt
        │       DEM_file03.png
        │       DEM_file03.txt
        │       ...
        │
        └── output
                ├── links_original
                ├── matfiles
                ├── binary
                ├── network
                └── others

```


