import pandas as pd
import numpy as np
import scipy.io
import matplotlib.pyplot as plt
#Temporary for testing with IEEE118 case
#DONE: TODO: Only show data for the failure states you actually reach -- for any others, make it blank
#TODO: Start at the number of initial failures, stop where it always stops (cascadestop=1)
#TODO: test a range of initial line failures until stops immediately -- overlay the graphs
#NOTE: T variable lets you see the differences between random initial failures and cascading failures resulting from simulation in the SACE model!
#TODO: maybe change T variable into single number representing how wide it is (see the variance)
#TODO: plot p-stop as function of variance of T
#NOTE: on previous: for small variance (.1) failures are concentrated, say there are 2 groups -- concentrated in region 5 and region 3 (and maybe mroe groups, n groups for n clusters)
#NOTE (Continued): Look at p-stop for all subgroups, do they all agree? -- if not, looking at variance alone is wrong!
#superposition, aggregate, or something else?
#TODO: answer the question: does variance matter?
#TODO: Part 1: initial conditions rich set for IEEE39/IEEE118; Part 2: Look into question we discussed: look at p-stop as function of variance/mean of Topological variable
#TODO: Cmax, F P-stop curve, generate evolution using p-stop data
#TODO: transition to different clusters
#TODO: use the markov chain model -- generate transition matrix
#TODO: steady-state distribution of blackout size
#TODO: mean failures as function of time
#TODO: calculate mean evolution of failures in Markov Chain compared to empirical
#TODO: fix bug in simulator that prevents accurate index of failure readouts
#TODO: see mean/variance of T PMF with T and F
#TODO: add to simulator: specify initial T to set locations of initial failures -- randomly select lines based on T -- different lines for different sims, but same number of line failures per cluster
#TODO: Markov chain model and Topology in parallel -- then combine the two
#TODO: create mapping of mean and variance of initial T and output T mean and variance -- curve fitting
#IEEE39 number of lines
#TODO: create matrix for 2 failures, 4 clusters (bins) mapping mean and variance of initial T to output T mean and variance
number_of_lines = 46
#number_of_lines = 186
mat = scipy.io.loadmat('case39_initial_failures_count_10_sm') #the states matrix input -- temporary
#mat = scipy.io.loadmat('states_IEEE118') #the states matrix input -- temporary
#print(mat)
states_column_names = ['Total Line Failures', 'Maximum failed line capacity', 
    'Load shed from previous step', 'Difference in Load Shed', 
    'Load', 'Free Space 1', 'Free Space 2', 'Steady State', 
    'Capacity of Failed Ones', 'Capacity of Failed Ones 2', 'Failed Line Index', 
    'Capacity of Failed One', 'Time of Failure Event', 
    'Accumulation of Failed Capacities', 'Free Space 3', 'Demand-Loadshed Difference',
    'Free Space 4', 'Generation']
data = mat['States']
states_df = pd.DataFrame(data=data, columns=states_column_names)
states_df = states_df.astype({'Total Line Failures' : int, 'Maximum failed line capacity' : float, 
    'Load shed from previous step' : float, 'Difference in Load Shed' : float, 
    'Load' : float, 'Free Space 1' : int, 'Free Space 2' : int, 'Steady State' : int, 
    'Capacity of Failed Ones' : float, 'Capacity of Failed Ones 2' : float, 'Failed Line Index' : int, 
    'Capacity of Failed One' : float, 'Time of Failure Event' : float, 
    'Accumulation of Failed Capacities' : float, 'Free Space 3' : int, 'Demand-Loadshed Difference' : float,
    'Free Space 4' : int, 'Generation' : float})
#print(states_df)
states_df.drop(columns=['Free Space 1', 'Free Space 2', 'Free Space 3', 'Free Space 4'], inplace=True)
#print(states_df.dtypes)
states_df.to_csv(r'states_dataframe', index=False)
#print(states_df['Total Line Failures'])
##Cascading Failure Curve Code
total_states = [0] * (number_of_lines + 1)
stable_states = [0] * (number_of_lines + 1)
min_index = number_of_lines
max_index = 0
for index, row in states_df.iterrows():
    #print(row['Total Line Failures'])
    total_line_failures = row['Total Line Failures'].astype(int)
    if total_line_failures < min_index:
        min_index = total_line_failures
    if total_line_failures > max_index:
        max_index = total_line_failures
    steady_state = row['Steady State'].astype(int)
    if(total_line_failures > 0):
        total_states[total_line_failures] = total_states[total_line_failures] + 1
        if (steady_state == -1):
            stable_states[total_line_failures] = stable_states[total_line_failures] + 1
cascade_stop = [0]*(number_of_lines + 1)
for i in range(number_of_lines):
    if (total_states[i] != 0):
        cascade_stop[i]=stable_states[i]/total_states[i]
##Plotting code
cascading_failure_df=pd.DataFrame({'x_values' : range(min_index, max_index+1), 'cascade_stop' : cascade_stop[min_index:max_index+1]})
fig = plt.figure()
plt.plot('x_values', 'cascade_stop', data=cascading_failure_df, color='skyblue', linewidth=1)
plt.xlabel('Number of Failed Lines')
plt.ylabel('Cascade-Stop Probability')
plt.title('Cascade-Stop Probability vs Number of Line Failures')
# show legend
plt.legend()
#set title
plt.title = "Cascade-Stop Probability vs Number of Line Failures"
# show graph
plt.show()




