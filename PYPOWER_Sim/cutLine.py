#TODO: convert S_cutLine.m to python
import numpy as np
import pypower as pp
import pandas as pd

# This function removes the transmission lines given by FailIndex from
# Adjacency matrix and MPC
def S_cutLine(AdjMatrix, mpc1, FailIndex):
    LargeNumber1 = float('inf')  # This number is used for generating failures by multiplying the impedence wiht them
    # Change the adjacent matrix
    # TODO: change it later according to the code
    AdjMatrix = np.ones((5, 5))
    # TODO: change it later according to the code
    AdjMatrix[2][2] = 0
    AdjMatrix[4][5] = 0
    #AdjMatrix(mpc1.branch(FailIndex,1),mpc1.branch(FailIndex,2))=0
    #AdjMatrix(mpc1.branch(FailIndex, 1), mpc1.branch(FailIndex, 2)) = 0
    
    # change the MPC
    #mpc1.branch(FailIndex,3)=mpc1.branch(FailIndex,3)*LargeNumber1; % resistance
    #mpc1.branch(FailIndex,4)=mpc1.branch(FailIndex,4)*LargeNumber1; % reactance
    #fix -- just choose very large value
    mpc1.branch(FailIndex,3)=LargeNumber1; # resistance
    mpc1.branch(FailIndex,4)=LargeNumber1; # reactance
    # line capacity rating
    mpc1.branch(FailIndex,6)=mpc1.branch(FailIndex,6)/mpc1.branch(FailIndex,6)
    mpc=mpc1
    AdjMat=AdjMatrix
    
    return AdjMat, mpc
