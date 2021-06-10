#TODO: Convert S_FindingStateSpace_ANN_dataset_function to python
import random
import numpy as np
import pypower as pp
import pandas as pd
import multiprocessing as mp
from numpy import array as arr

def FindStateSpace (CaseName, Iterations, InitialFailures, LoadGenerationRatio, LoadShedConstant, EstimationError):
    FakeCapRate = 1; # fake capacity
    # Parameter initialization 
    trueCaps= arr(50., 100., 200., 400., 800.) # quantized capacity
    # Load the case
    mpc1 = loadcase(CaseName)
    #Ready the case
    mpc1 = readyTheCase(mpc1)
    #keep original values of buses, gens, and branches before changing
    originalNumBus = len(mpc1.bus)
    originalNumGen = len(mpc1.gen)
    originalNumBranches = len(mpc1.branches)
    numBuses = originalNumBus
    numLine = originalNumLine
    #separate the buses with both load and generators into separate load and generator buses
    (mpc1, loadGenMatch) = separateGenAndLoad(mpc1)
    (whichInitialLoad, generation, demand, demandIndex) = findFullLoadOfGrid(mpc1)
    #Calculate total demand and generation capacity of grid
    mpc1 = loadcase(CaseName)
    mpc1 = readyTheCase(mpc1)
    #check if any negative load and convert to positive load -- might not be necessary
    for bus in mpc1.bus:
        if (bus[2] < 0):
            bus[2]= abs(bus[2]) #Convert to positive value
    #Seperate the buses with both load and generators into seperate load and generator buses -- not necessary since case includes separated gens and loads already?
    (mpc1, loadGenMatch) = separateGenAndLoad(mpc1)
    
    #Find installed capacity of a transmission line and use it as rateA threshold
    (Capacity, FlowCap) = capFinder(whichInitialLoad,mpc1,trueCaps,originalNumBranches) #originalNumBranch converted to originalNumLine
    #Not dealing with this yet -- fake capacity rate
    mpc1.branch[:,6] = FakeCapRate*Capacity #Figure out how to properly get this information
    countCaps = []
    for trueCap in trueCaps:
        countCaps.append(sum(Capacity == trueCap))
    #%% Reset mpc1, PD: take mpc with separated load and generator
    OriginalMPC = mpc1 #this is the MPC with separated load and generator
    #clear mpc1;
    #set r value(s) (load/gen ratio)
    DGRatioVector = [LoadGenerationRatio]
    len_DGRatioVector = len(DGRatioVector)
    #set e value(s) (capacity estimation error)
    DeltaVector = [EstimationError]
    len_DeltaVector = len(DeltaVector)
    #set \theta values (load shedding)
    NoCoopPercentageVector = [LoadShedConstant]
    len_NoCoopPercentageVector = len(NoCoopPercentageVector)
    #beta vector
    betavector = [0]
    beta = betavector(random.randint(0, len(betavector)-1))
    
    numIt = Iterations
    #Generate initial failure table
    iniFailNodes = []
    for i in range(0, numIt-1):
        b = InitialFailures
        randomIndex = np.random.permutation(numLine)
        temp = randomIndex[0:b]
        IniFidx = randomIndex[0:b]

        IniFtable[1,i] = IniFidx
    mpc1 = OriginalMPC
    #Get branch matrix
    BranchMatrix = mpc1.branch
    NumBranches = len(BranchMatrix[:,0])
    #Get bus matrix
    BusMatrix = mpc1.bus
    NumBuses = len(BusMatrix[:,0])
    #Get Gen Matrix
    GenMatrix = mpc1.gen
    NumGens = len(GenMatrix[:,0])
    #Create state variables
    #Difference here -- using data frame
    column_names = (["Failure List", 
        "Total Capacity of Failed Lines",
        "Load Shed",
        "Difference in Load Shed",
        "Load",
        "Steady State",
        "Index of Failed Line",
        "Capacity of Failed Line",
        "Time of Failure Event",
        "Accumulation of Failed Capacities"])
    empty_states = pd.dataframe(columns=column_names)
    #Start up parallel pool
    iteration_pool = mp.Pool()
    #run the cascading failures
    iteration_states = iteration_pool.map(cascadingFailure, range(numIt))
    #return a list of the cascading failure state matrices, which are in dataframe format
    return iteration_states

def cascadingFailure(OriginalMPC, NumBranches, NoCoopPercentageVector, TrueCaps, DGRatioVector, WhichInitialLoad, Capacity, IniFtable, len_DGRatioVector, len_DeltaVector, DeltaVector, len_NoCoopPercentageVector, FlowCap, DemandIndex):
    result = DC_powerFlow_calculator(OriginalMPC, NumBranches, NoCoopPercentageVector, TrueCaps, DGRatioVector, WhichInitialLoad, Capacity, IniFtable, len_DGRatioVector, len_DeltaVector, DeltaVector, len_NoCoopPercentageVector, FlowCap, DemandIndex, empty_states)
    return result





    




