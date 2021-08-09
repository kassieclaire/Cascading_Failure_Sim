import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#x = input = [mu; var] = 2x1 vector
#y = f(x) = 2x1 vectir
#A = 2x2 matrix
#b = 2x1 vector

#NOTE: Curve fit function y = A*x+b
#NOTE: mappings different for every starting number of failures
from scipy.optimize import curve_fit as cf
def curve_fit_mu_and_var():
    #take input from states dataframe
    states_df = pd.read_csv('states_simple.csv')
    #TODO: map mu and variance to new mu and variance

    ##initialize variables
    #original state
    original_mu_vector = [] #this vector is for the mu for the original state
    original_var_vector = [] #this vector is for the var for the original state
    #next states
    next_mu_vector = [] #this vector is for the mu for the next state
    next_var_vector = [] #this vector is for the var for the next state
    #NOTE: if this is steady state, then next mu and var for this state are same as original mu and variance for this state
    for index, row in states_df.iterrows():
        original_mu = row['Mean of T']
        original_var = row['Variance of T']
        if row['Steady State'] == -1: #if steady state
            #set next mu and var values to original values
            next_mu = original_mu
            next_var = original_var
        else: #if not steady state
            #set next mu and var values to next state's values
            next_mu = states_df.iloc[[index+1]]['Mean of T']
            next_var = states_df.iloc[[index+1]]['Variance of T']

        #append values to appropriate vectors
        original_mu_vector.append(original_mu)
        original_var_vector.append(original_var)
        next_mu_vector.append(next_mu)
        next_var_vector.append(next_var)
    print(len(original_mu_vector))
    print(len(next_mu_vector))




