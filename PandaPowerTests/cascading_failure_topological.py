##TODO: Goals:
#Generate PStop as function of F
#Generate pStop as function of CMax
#Generate pStop as function of F and CMax
#Generate pStop as function of first component of T (hence 2nd component if only 2 clusters)
#Generate pStop as function of F and T components -- ultimate resolution
#Many different ways to generate pStop
import pandas as pd
import numpy as np
import scipy.io
import matplotlib.pyplot as plt
from operator import truediv
##Temporary for testing with IEEE118 case
number_of_lines = 186
initial_failures = [] #indices of initial failures
##testing clusters
#clusters = {'a' : range(0, 93), 'b' : range(93, number_of_lines+1)}
#clusters = {range(0, 93) : 'a', range(93, number_of_lines+1) : 'b'}'
clusters = [list(range(0, 94)), list(range(94, number_of_lines+1))]
print(clusters[0])
##Temporarily loading in matrix
mat = scipy.io.loadmat('states.mat') #the states matrix input -- temporary
initial_failures_mat = scipy.io.loadmat('initial_failures') #cell of arrays containing the initial failures for each iteration
initial_failures_arrays = [l.tolist() for l in initial_failures_mat['Initial_Failure_Table']]
initial_failures = [l.tolist()[0] for l in initial_failures_arrays[0]]
print(initial_failures)
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
states_df.to_csv(r'states_dataframe.csv', index=False)
##Create new dataframe for cluster line failure information
#cluster_failures = [[0]*number_of_lines for x in range(len(clusters))] #list of lists of cluster line failures
cluster_failures = []
cluster_failures_topological_factors = []
#cluster_failures = []
##Failures in clusters code
start_detect = 1
line_failure_row = [0]*len(clusters) # set line_failure_row outside since it needs to be kept between iterations
#iteration tracker for selecting the correct initial_failures list to use
iteration_track = 0
for index, row in states_df.iterrows():
    steady_state = row['Steady State'].astype(int)
    total_line_failures = row['Total Line Failures'].astype(int)
    line_failure_index = row['Failed Line Index'].astype(int)
    #print(line_failure_index)
    if start_detect == 1: #if previous state was steady state
        if steady_state != -1: #if this is not a steady state, do not reset the next iteration
            start_detect = 0 #set start_detect to 0
        #reset the line failures and then do the for loop for adding for the initial failure
        line_failure_row = [0]*len(clusters)
        for failure in initial_failures[iteration_track]:
             for i in range(len(clusters)):
                if failure in clusters[i]: #if line failure is in cluster i
                    line_failure_row[i] = line_failure_row[i]+1
        iteration_track = iteration_track+1 #increment iteration tracker -- this iteration is now complete
    else: #if previous state was not steady state
        if steady_state == -1: #if steady state, set restart variable to 1
            start_detect = 1
        for i in range(len(clusters)):
            if line_failure_index in clusters[i]: #if line failure is in cluster i
                #print("Incrementing cluster ", i)
                line_failure_row[i] = line_failure_row[i]+1
    cluster_failures.append(line_failure_row) #append line_failure_row to the cluster_failures list of lists (matrix to be added)
    topological_factor_row = [cluster_failure / total_line_failures for cluster_failure in line_failure_row] #create the topological factor row
    cluster_failures_topological_factors.append(topological_factor_row)
print("Iteration track = ", iteration_track) #check, should be the number of iterations run
#print(cluster_failures)
#print(cluster_failures_topological_factors)

cluster_line_failure_df = pd.DataFrame()
#print(states_df['Total Line Failures'])
##Cascading Failure Curve Code
total_states = [0] * (number_of_lines + 1)
stable_states = [0] * (number_of_lines + 1)
for index, row in states_df.iterrows():
    #print(row['Total Line Failures'])
    total_line_failures = row['Total Line Failures'].astype(int)
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
cascading_failure_df=pd.DataFrame({'x_values' : range(0, number_of_lines+1), 'cascade_stop' : cascade_stop})
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




