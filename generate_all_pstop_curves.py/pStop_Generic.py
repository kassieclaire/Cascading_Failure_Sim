import pandas as pd
import numpy as np
import scipy.io
import matplotlib.pyplot as plt
from math import log10, floor
#DONE: TODO: Add probabilities for failure in specific regions based on distribution of current failures in regions
#DONE: TODO: Cluster lines based on bus clusters
#Talk to Brad or Matt to get into workstation, get IP address of workstation in lab -- ask Jamir
#TODO: probability mass distribution given fixed number of failures -- with Jamir/AJ
#TODO: 02-09-2022: Be able to set F for the Pstop using this function -- such that we can look at the curve for a specific F
#TODO: 02-09-2022: B able to set mean/variance for Pstop so that we can look at pstop over range of variance (fix mean/F) and mean (fix variance/F) values
def generate_generic_pStop(states_df, variable_name = 'Total Line Failures', amount_to_round = 1):
    
    variable_vector = []
    #check if float64
    if isinstance(states_df[variable_name][0], float):
        print("Values are float, rounding to ", amount_to_round, " decimal place")
        variable_vector = [round(val, amount_to_round) for val in states_df[variable_name]]
    else:
        variable_vector = states_df[variable_name]
    
    #get unique accumulation of Capacity values
    print(type(variable_vector[0]))
    unique_values = set(variable_vector)
    unique_values = list(unique_values)
    #print(unique_values)
    ##Cascading Failure Curve Code
    #generate empty list
    states_initialization_vector = [0] * (len(unique_values))
    #zip them up into dictionaries with accumulated line capacity values as keys and 0 as default value
    total_states = dict(zip(unique_values, states_initialization_vector))
    stable_states = dict(zip(unique_values, states_initialization_vector))
    cascade_stop = dict(zip(unique_values, states_initialization_vector))
    
    for index, row in states_df.iterrows():
        #print(row['Total Line Failures'])
        #total_line_failures = int(row['Total Line Failures'])
        #variable_value = int(row[variable_name])
        variable_value = variable_vector[index]
        steady_state = int(row['Steady State'])
        if(variable_value > 0):
            total_states[variable_value] = total_states[variable_value] + 1
            if (steady_state == -1):
                stable_states[variable_value] = stable_states[variable_value] + 1
    
    for i in unique_values:
        if (total_states[i] != 0):
            cascade_stop[i]=stable_states[i]/total_states[i]
    ##Plotting code
    #print(cascade_stop)
    sorted_cascade_stop = sorted(cascade_stop.items())
    #print(sorted_cascade_stop)
    cascading_failure_df=pd.DataFrame.from_dict({'x_values' :  [a_tuple[0] for a_tuple in sorted_cascade_stop], 'cascade_stop' :  [a_tuple[1] for a_tuple in sorted_cascade_stop]})
    return cascading_failure_df