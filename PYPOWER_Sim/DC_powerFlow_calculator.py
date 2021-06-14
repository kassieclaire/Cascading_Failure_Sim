#TODO: Convert S_DCPOWERFLOWSIMULATION_ANN_DATASET.m to python
import numpy as np
import pypower as pypower
import scipy as sp


##set default values/bug checking
PSF_time = 0
PSF_stress = 0
PSF_complexity = 0
PSF_experience = 0
PSF_procedures = 0
PSF_ergonomics = 0
PSF_fitness = 1
PSF_work_process = 0

PSF = [PSF_time, PSF_stress, PSF_complexity, PSF_experience, PSF_procedures, PSF_ergonomics, PSF_work_process]
randArray = np.zeros(len(PSF))

'''
inputs into main function
taken out for testing
-->OriginalMPC, NumBranches, NoCoopPercentageVector, StateCounter, TrueCaps, DGRatioVector, WhichInitialLoad, Capacity, s, IniFtable, len_DGRatioVector, len_DeltaVector, DeltaVector, len_NoCoopPercentageVector, FlowCap, DemandIndex
'''
def DC_powerFlow_calculator(OriginalMPC, NumBranches, NoCoopPercentageVector, StateCounter, TrueCaps, DGRatioVector, WhichInitialLoad, Capacity, s, IniFtable, len_DeltaVector, DeltaVector, len_NoCoopPercentageVector, FlowCap, DemandIndex):
    #array of random values
    for x in range(0, len(PSF)):
        randArray[x] = np.random.uniform(0,1)
    
    print(randArray)
# available time
    if randArray[0] <=.42:
        PSF_time = 10
    elif randArray[0]>.42 and randArray[0]<= .97:
        PSF_time = 1
    else:
        PSF_time = .1
    PSF[0] = PSF_time
#stress
    if randArray[1] <=.03:
        PSF_stress = 5
    elif randArray[1]>.03 and randArray[1]<= .34:
        PSF_stress = 2
    else:
        PSF_stress = 1
    PSF[1] = PSF_stress

#complexity

    if randArray[2] <=.11:
        PSF_complexity = 5
    elif randArray[2]>.11 and randArray[2]<= .78:
        PSF_complexity = 2
    elif randArray[2]>.78 and randArray[2]<= .92:
        PSF_complexity  = 1
    else:
        PSF_complexity = 0.1
    PSF[2] = PSF_complexity

#experience
    if randArray[3] <=.11:
        PSF_experience = 10
    elif randArray[3]>.11 and randArray[3]<= .47:
        PSF_experience = 1
    else:
        PSF_experience = .5
    PSF[3] = PSF_experience

#procedures
    if randArray[4] <=.06:
        PSF_procedures = 50
    elif randArray[4] >.06 and randArray[4]<= .14:
        PSF_procedures = 20
    elif randArray[4]>.14 and randArray[4]<= .20:
        PSF_procedures  = 5
    else:
        PSF_procedures = 1
    PSF[4] = PSF_procedures
    
#ergonomics
    
    if randArray[5] <=.36:
        PSF_ergonomics = 50
    elif randArray[5]>.36 and randArray[5]<= .53:
        PSF_ergonomics = 10
    else:
        PSF_ergonomics = 1
    PSF[5] = PSF_ergonomics
#work_process

    if randArray[6] <=.11:
        PSF_work_process = 2
    elif randArray[6]>.11 and randArray[6]<= .80:
        PSF_work_process= 1
    else:
        PSF_work_process = .8
    PSF[6] = PSF_work_process
    print(PSF)

    HEP = (0.01*(PSF_complexity*PSF_ergonomics*PSF_experience*PSF_fitness*PSF_procedures*PSF_stress*PSF_time*PSF_work_process))/ ((0.01*((PSF_complexity*PSF_ergonomics*PSF_experience*PSF_fitness*PSF_procedures*PSF_stress*PSF_time*PSF_work_process)-1))+1)
    HEP_org = HEP
    DGRatio = DGRatioVector(np.random.randint(1, len(DGRatioVector)))
    alpha = DeltaVector(np.random.randint(1, len(DeltaVector)))
    alphaOriginal = alpha
    noCoopPercentage = NoCoopPercentageVector(np.random.randint(1, len(NoCoopPercentageVector)))

    if noCoopPercentage > DGRatio:
        noCoopPercentage = DGRatioVector

    noCoPercenOrig = noCoopPercentage

    ##Human error
    HEP = 0 #dont include HEP if this is zero
    if HEP > 0.2:
        noCoopPercentage = round((noCoopPercentage + HEP*noCoopPercentage),2)
        alpha = round(alpha + HEP*alpha, 2)
        if noCoopPercentage > 0.9:
            noCoopPercentage = 0.9
        if alpha > 0.6:
            alpha = 0.6

    ##failures
    totalShed = 0
    listOfFailures = np.zeros(1,NumBranches)
    mpcl = OriginalMPC
    branchMatrix = mpcl.branch
    busMatrix = mpcl.bus
    genMatrix = mpcl.gen
    NumBranches = len(branchMatrix) ##find format for pypower which column needs to be included
    numGens= 

if __name__ =='__main__':
    DC_powerFlow_calculator()
