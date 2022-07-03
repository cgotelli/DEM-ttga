# IMPORT ----------------------------------------------------------------------
import numpy as np
import matplotlib.pyplot as plt
from os import listdir
from os.path import isfile, join
import math


#------------------------------------------------------------------------------
#                    Characterisation of channel evolution 
#------------------------------------------------------------------------------

# In this section, the functions computed are applications of concepts from the
# turbulence theory and are used to characterize the channel evolution.


#-----------------------Time average of bed elevations------------------------- 


def time_average(DEM_path, dt, delta_T, w, h):
    # computes the time averaging bed topography for 1 realization of channel 
    # evolution experiment 
    
    # --> dt is the time interval between two DEMs
    # --> delta_T is time period sufficiently long for the braided channel to 
    #     experience all the possible independent configurations
    # --> the time average can be computed from t0 to t0 + delta_T for t0 a 
    #     time far enough from the start of the simulation for which we observe 
    #     a statistically stationary braiding channel
    
    # DEM are detrended .txt files from the detrend function
    DEMs = [f for f in listdir(DEM_path) if isfile(join(DEM_path,f)) and f.endswith('.txt')]
    
    B = np.zeros((h,w))
    
    for DEM in DEMs :
        topo_list=[]
        with open(DEM_path + DEM, "r") as f:
            line = f.readline()
            for line in f:
                topo_list.append(line.split())
        topo = np.asarray(topo_list)
        topo = topo.astype(np.float)
        topo = topo*dt
        B = np.add(B, topo)

    B = B/(delta_T+dt)
    
    # return a matrix with time averaging topography
    return B



#----------------------Ensemble average of bed elevations----------------------
    

def ensemble_average(DEM_path, w, h):
    # computes the ensemble averaging bed topography at a given time 
    # for multiple independent realizations of channel evolution experiments 
    
    # DEM are detrended .txt files from the detrend function
    DEMs = [f for f in listdir(DEM_path) if isfile(join(DEM_path,f)) and f.endswith('.txt')]
    
    B = np.zeros((h,w))
    count = 0
    
    for DEM in DEMs :
        count += 1
        topo_list=[]
        with open(DEM_path + DEM, "r") as f:
            line = f.readline()
            for line in f:
                topo_list.append(line.split())
        topo = np.asarray(topo_list)
        topo = topo.astype(np.float)
        B = np.add(B, topo)

    B = B/count

    # return a matrix with time averaging topography
    return B



#--------------------------Fluctuating bed elevations--------------------------


def fluctuations(DEM, dt, delta_T, w, h, choice):
    # --> computes the fluctuating bed elevations for different DEMs based on
    #     either the ensemble average or the time average
    
    # DEM are detrended .txt files from the detrend function
    
    if choice == 'ensemble':
            B = ensemble_average(DEM_path, w, h)
    if choice == 'time':
            B = time_average(DEM_path, dt, delta_T, w, h)
            
    topo_list = []
    with open(DEM, "r") as f:
        line = f.readline()
        for line in f:
            topo_list.append(line.split())
    topo = np.asarray(topo_list)
    topo = topo.astype(np.float)
    b = topo - B
    
    return b



#---------------------Root-mean-square of bed fluctuations--------------------- 


def rms_fluctuations(DEM_path, dt, delta_T, w, h):
    # --> computes the RMS bed elevations for different DEMs based on time average
    # --> refers to one point-statistics because rms are evaluated independently 
    #     at each point
    
    DEMs = [f for f in listdir(DEM_path) if isfile(join(DEM_path,f)) and f.endswith('.txt')]
    
    # --> rms_fluctu is a matrix which will contains the rms bed fluctuations 
    #     values at each point
    rms_fluctu = np.zeros((h,w))
    
    for DEM in DEMs:
        fluctu = fluctuations(DEM_path+DEM, dt, delta_T, w, h, 'time')
        rms_fluctu = np.add(rms_fluctu, fluctu**2*dt)
    
    rms_fluctu = np.sqrt(rms_fluctu/(delta_T+dt))
    
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Root-mean-square bed fluctuations ' + r'$b_{rms}$' + ' [m]')
    plt.imshow(rms_fluctu)
    plt.colorbar()
    plt.show()
     
    return rms_fluctu


  
#----------------Time averaging approach : streamwise correlation--------------s 


def streamwise_correlation_time(DEM_path, dt, delta_T, w, h, r):
    # --> compute the streamwise correlation of bed fluctuations 
    # --> refers to two point-statistics because it computes correlations   
    #     between bed fluctuations at point (x,y) and bed fluctuations at  
    #     position (x + r, y)

    DEMs = [f for f in listdir(DEM_path) if isfile(join(DEM_path,f)) and f.endswith('.txt')]
    
    # streamwise_corr will contains the streamwise correlation values at each point
    streamwise_corr = np.zeros((h,w))
    
    # bb_r will contain the sum of bed fluctuations at position (x, y) multiply  
    # by bed fluctuations at position (x + r, y) 
    bb_r = np.zeros((h,w))
    
    # b2 will contain the sum of squared bed fluctuations at position (x, y)
    b2 = np.zeros((h,w))
    
    # b_r2 will contain the sum of squared bed fluctuations at position (x + r, y)
    b_r2 = np.zeros((h,w))
    
    for DEM in DEMs:
        fluctu = fluctuations(DEM_path+DEM, dt, delta_T, w, h, 'time')
        fluctu_r = np.copy(fluctu)
        for i in range(0,h):
            for j in range(0,w-r):
                fluctu_r[i][j] = fluctu[i][j+r]
        
        bb_r = np.add(bb_r, np.multiply(fluctu, fluctu_r))
        b2 = np.add(b2, np.multiply(fluctu, fluctu))
        b_r2 = np.add(b_r2, np.multiply(fluctu_r, fluctu_r))
    
    streamwise_corr = np.divide(bb_r, np.sqrt(np.multiply(b2, b_r2)))

    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Streamwise Correlation - time averaging approach')
    plt.imshow(streamwise_corr)
    plt.colorbar()
    plt.show()
         
    return streamwise_corr



#------------Time averaging approach : cross channel correlation---------------


def cross_channel_correlation_time(DEM_path, dt, delta_T, w, h, r):
    # --> compute the cross channel correlation of bed fluctuations 
    # --> refer to two point-statistics because it computes correlations  
    #     between bed fluctuations at point (x, y) and bed fluctuations at position 
    #     y + r

    DEMs = [f for f in listdir(DEM_path) if isfile(join(DEM_path,f)) and f.endswith('.txt')]
    
    # cross_channel_corr will contain the cross channel correlation values at 
    # each point
    cross_channel_corr = np.zeros((h,w))
    
    # bb_r will contain the sum of bed fluctuations at position (x, y) multiply  
    # by bed fluctuations at position (x, y + r) 
    bb_r = np.zeros((h,w))
    
    # b2 will contain the sum of squared bed fluctuations at position (x, y)
    b2 = np.zeros((h,w))
    
    # b_r2 will contain the sum of squared bed fluctuations at position (x, y + r)
    b_r2 = np.zeros((h,w))
    
    for DEM in DEMs:
        fluctu = fluctuations(DEM_path+DEM, dt, delta_T, w, h, 'time')
        fluctu_r = np.copy(fluctu)
        for i in range(0,h-r):
            for j in range(0,w):
                fluctu_r[i][j] = fluctu[i+r][j]
        
        bb_r = np.add(bb_r, np.multiply(fluctu, fluctu_r))
        b2 = np.add(b2, np.multiply(fluctu, fluctu))
        b_r2 = np.add(b_r2, np.multiply(fluctu_r, fluctu_r))
    
    cross_channel_corr = np.divide(bb_r, np.sqrt(np.multiply(b2, b_r2)))
    
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Cross Channel Correlation - time averaging approach')
    plt.imshow(cross_channel_corr)
    plt.colorbar()
    plt.show()
     
    return cross_channel_corr



#--------------Ensemble averaging approach : streamwise correlation------------


def streamwise_correlation_ensemble(DEM_path, dt, delta_T, w, h, r):
    
    DEMs = [f for f in listdir(DEM_path) if isfile(join(DEM_path,f)) and f.endswith('.txt')]
    
    streamwise_corr = np.zeros((h,w))
    bb_r = np.zeros((h,w))
    b2 = np.zeros((h,w))
    b_r2 = np.zeros((h,w))
    
    
    for DEM in DEMs:
        fluctu = fluctuations(DEM_path+DEM, dt, delta_T, w, h, 'ensemble')
        fluctu_r = np.copy(fluctu)
        for i in range(0,h):
            for j in range(0,w-r):
                fluctu_r[i][j] = fluctu[i][j+r]
        
        bb_r = np.add(bb_r, np.multiply(fluctu, fluctu_r))
        b2 = np.add(b2, np.multiply(fluctu, fluctu))
        b_r2 = np.add(b_r2, np.multiply(fluctu_r, fluctu_r))
    
    streamwise_corr = np.divide(bb_r, np.sqrt(np.multiply(b2, b_r2)))
    
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Streamwise Correlation - ensemble averaging approach')
    plt.imshow(streamwise_corr)
    plt.colorbar()
    plt.show()
    
    return streamwise_corr



#-----------Ensemble averaging approach : cross channel correlation------------ 


def cross_channel_correlation_ensemble(DEM_path, dt, delta_T, w, h, r):
    
    DEMs = [f for f in listdir(DEM_path) if isfile(join(DEM_path,f)) and f.endswith('.txt')]
    
    cross_channel_corr = np.zeros((h,w))
    bb_r = np.zeros((h,w))
    b2 = np.zeros((h,w))
    b_r2 = np.zeros((h,w))
    
    
    for DEM in DEMs:
        fluctu = fluctuations(DEM_path+DEM, dt, delta_T, w, h, 'ensemble')
        fluctu_r = np.copy(fluctu)
        for i in range(0,h-r):
            for j in range(0,w):
                fluctu_r[i][j] = fluctu[i+r][j]
        
        bb_r = np.add(bb_r, np.multiply(fluctu, fluctu_r))
        b2 = np.add(b2, np.multiply(fluctu, fluctu))
        b_r2 = np.add(b_r2, np.multiply(fluctu_r, fluctu_r))
    
    cross_channel_corr = np.divide(bb_r, np.sqrt(np.multiply(b2, b_r2)))
    
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Cross Channel Correlation - ensemble averaging approach')
    plt.imshow(cross_channel_corr)
    plt.colorbar()
    plt.show()
    
    return cross_channel_corr



#-----------------------------Plot r vs correlation----------------------------


def plot_r_vs_correlation(choice, r_list, x_interval, y_interval, DEM_path, dt, delta_T, w, h):
    # plot the averaged correlations on a domain and for different r values
    # --> r_list defines the list of r values for the correlations' computation  
    # --> x_interval and y_interval define the domain on which the correlation 
    #     will be averaged
    
    mean_correlation = []
    
    for r in r_list:
        if choice == 'streamwise correlation time':
            streamwise_corr = streamwise_correlation_time(DEM_path, dt, delta_T, w, h, r)
            plt.xlabel('Distance streamwise [m]')
            plt.ylabel('Correlation spatially averaged')
            plt.title('Streamwise correlation spatially averaged - time averaging approach')
        
        if choice == 'cross channel correlation time':
            streamwise_corr = cross_channel_correlation_time(DEM_path, dt, delta_T, w, h, r)
            plt.xlabel('Distance cross-channel [m]')
            plt.ylabel('Correlation spatially averaged')
            plt.title('Cross-channel correlation spatially averaged - time averaging approach')
        
        if choice == 'streamwise correlation ensemble':
            streamwise_corr = streamwise_correlation_ensemble(DEM_path, dt, delta_T, w, h, r)
            plt.xlabel('Distance streamwise [m]')
            plt.ylabel('Correlation spatially averaged')
            plt.title('Streamwise correlation spatially averaged - ensemble averaging approach')
        
        if choice == 'cross channel correlation ensemble':
            streamwise_corr = cross_channel_correlation_ensemble(DEM_path, dt, delta_T, w, h, r)
            plt.xlabel('Distance cross-channel [m]')
            plt.ylabel('Correlation spatially averaged')
            plt.title('Cross-channel correlation spatially averaged - ensemble averaging approach')
        
        streamwise_corr = streamwise_corr[y_interval[0]:y_interval[1], x_interval[0]:x_interval[1]]
        mean = np.nanmean(streamwise_corr)
        mean_correlation.append(mean)
    
    plt.plot(r_list, mean_correlation)
    plt.show()
    
    return mean_correlation




#------------------------------------------------------------------------------
#                  Characterisation of the chaotic behavior 
#------------------------------------------------------------------------------

# In this section, the functions computed show the chaotic behavior of braided 
# channel evolution and are used to prove the sensitive dependence on the 
# initial conditions and the aperiodic long-term behavior.


#---------------Root-mean-square difference in bed topography------------------


def rms_topography(DEM, DEMref):
    # compute the root-mean square difference at a given time of the bed 
    # topography compared to another topography taken as reference
    # --> DEM_ref is a DEM of the topography taken as reference
    
    topo_list=[]
    
    # DEM and DEMref are detrended .txt files from the detrend function
    with open(DEM, "r") as f:
        line = f.readline()
        for line in f:
            topo_list.append(line.split())
    topo = np.asarray(topo_list)
    topo = topo.astype(np.float)
    
    topo_list=[]
    
    with open(DEMref, "r") as f:
        line = f.readline()
        for line in f:
            topo_list.append(line.split())
    topo_ref = np.asarray(topo_list)
    topo_ref = topo_ref.astype(np.float)
    
    rows, columns = np.shape(topo)
    
    sum_f = 0
    
    for i in range (0,columns):
        for j in range(0, rows):
            if math.isnan(topo[j][i]):
                topo[j][i] = 0
            if math.isnan(topo_ref[j][i]):
                topo_ref[j][i] = 0
            sum_f += ( topo[j][i] - topo_ref[j][i] )**2


    return np.sqrt(sum_f/(rows*columns))
    
    
    
#------Time trend of the root-mean-square difference in the bed topography-----




#---------------------------Bed elevation changes------------------------------ 


def plot_elevation_changes(path, coordinates):
    # plot a time series of bed elevation changes at different locations
    # --> 'coordinates' is a list of coodinates defining the different  
    #     locations of the time series
    
    DEMs = [f for f in listdir(path) if isfile(join(path,f)) and f.endswith('.txt')]
    DEMs.sort()

    bed_changes = [] 
    
    DEM_name = [] # to change for defining the horzontal axis
    
    ref = []
    
    with open(path + DEMs[0], "r") as f:
        line = f.readline()
        for line in f:
            ref.append(line.split())
        topo_ref = np.asarray(ref)
        topo_ref = topo_ref.astype(np.float)
    
    # every DEM correspond to a bed topography a at given time
    for DEM in DEMs:
        DEM_name.append(float(DEM[-8:-4])) # to change for defining the horzontal axis
        topo_list=[]
        with open(path + DEM, "r") as f:
            line = f.readline()
            for line in f:
                topo_list.append(line.split())
        topo = np.asarray(topo_list)
        topo = topo.astype(np.float)
        topo = np.subtract(topo, topo_ref)
        bed_changes_list = []
        for coord in coordinates:
            bed_changes_list.append(topo[coord[1]][coord[0]])
        bed_changes.append(bed_changes_list)
        
    bed_changes = np.asarray(bed_changes)
    
    for i in range(0,len(coordinates)):
        plt.plot(DEM_name, bed_changes[:,i], label = 'x = ' + str(coordinates[i][0]) + ' y = ' + str(coordinates[i][1]))
    plt.xlabel('Time [s]')
    plt.ylabel('Bed elevation changes [m]')
    plt.legend()
    plt.show()
    
    
#------------------------Maximum Lyapunov exponent-----------------------------



#-------------------------Power spectral density-------------------------------




#------------------------------------------------------------------------------
#                                Tests 
#------------------------------------------------------------------------------

DEM_path = '/home/lhe/Documents/ttga_DEM/toProcess/Tests/'
DEM = 'detrended_0.94.txt'
r_list = [0,1,2,5,10,20]
choice = 'streamwise correlation time'
coordinates = np.array([[100,100], [200,200], [300,300], [400,400], [500,500]])

#print(rms_topography( path_DEM + file, path_DEM + 'detrended_dsm01.txt' ))
#print(time_average(DEM_path, 0.02, 0.2, 646, 564))
#print(ensemble_average(DEM_path, 646, 564))
#print(fluctuations(DEM_path + DEM, 0.02, 0.2, 646, 564, 'time'))
#print(rms_fluctuations(DEM_path, 0.02, 0.2, 646, 564))
#print(streamwise_correlation_time(DEM_path, 0.02, 0.2, 646, 564, 10))
#print(plot_r_vs_correlation(choice,r_list, [100,500], [100,500], DEM_path, 0.02, 0.2, 646, 564))
#print(cross_channel_correlation_time(DEM_path, 0.02, 0.2, 646, 564, 10))
#print(streamwise_correlation_ensemble(DEM_path,  0.02, 0.2, 646, 564, 100))
#print(cross_channel_correlation_ensemble(DEM_path,  0.02, 0.2, 646, 564, 100))
#print(plot_elevation_changes(DEM_path, coordinates))

