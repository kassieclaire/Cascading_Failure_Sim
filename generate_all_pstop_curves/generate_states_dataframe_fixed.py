import pandas as pd
import numpy as np
import scipy.io
import matplotlib.pyplot as plt
import os, sys
#DONE: TODO: Add probabilities for failure in specific regions based on distribution of current failures in regions
#DONE: TODO: Cluster lines based on bus clusters
#Talk to Brad or Matt to get into workstation, get IP address of workstation in lab -- ask Jamir
#TODO: probability mass distribution given fixed number of failures -- with Jamir/AJ
def generate_states_df(states_matrix_name='states',initial_failure_table_name='initial_failures', clusters_matrix_name='cluster_branch_118', number_of_lines=186, use_test_cluster=False, output_df_name = "states_dataframe", use_simplified_df = False, states_matrix_folder = 'states_matrices', save_as_csv = False):
    #number of errors
    num_errors = 0
    #change directory to include folder in path
    old_dir = os.getcwd()
    os.chdir(os.getcwd() + os.path.sep + states_matrix_folder)
    if states_matrix_folder != '':
        os.chdir(os.path.join(os.path.dirname(__file__), states_matrix_folder))
    ##Load in clusters
    if use_test_cluster:
        clusters = [list(range(0, 94)), list(range(94, number_of_lines+1))]
    else:
        cluster_mat = scipy.io.loadmat(clusters_matrix_name)
        cluster_lists = [l.tolist() for l in cluster_mat[clusters_matrix_name][0]]
        clusters = [[item for sublist in cluster_list for item in sublist] for cluster_list in cluster_lists]
    #print(clusters)
    #print(len(clusters))
    #clusters = cluster_mat[]
    
    #test with 3 clusters
    #clusters = [list(range(0, 50)),list(range(50, 94)), list(range(94, number_of_lines+1))]
    #print(clusters[0])
    ##Temporarily loading in matrix
    mat = scipy.io.loadmat(states_matrix_name) #the states matrix input -- temporary
    initial_failures_mat = scipy.io.loadmat(initial_failure_table_name) #cell of arrays containing the initial failures for each iteration
    initial_failures_arrays = [l.tolist() for l in initial_failures_mat['Initial_Failure_Table']]
    initial_failures = [l.tolist()[0] for l in initial_failures_arrays[0]] #change initial failure matrix into list of lists
    
    #change directory back now
    os.chdir(old_dir)

    #print(initial_failures)
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
    states_df = states_df.astype({'Total Line Failures' : int, 'Maximum failed line capacity' : int, 
        'Load shed from previous step' : float, 'Difference in Load Shed' : float, 
        'Load' : float, 'Free Space 1' : int, 'Free Space 2' : int, 'Steady State' : int, 
        'Capacity of Failed Ones' : float, 'Capacity of Failed Ones 2' : float, 'Failed Line Index' : int, 
        'Capacity of Failed One' : float, 'Time of Failure Event' : float, 
        'Accumulation of Failed Capacities' : int, 'Free Space 3' : int, 'Demand-Loadshed Difference' : float,
        'Free Space 4' : int, 'Generation' : float})
    #print(states_df)
    states_df.drop(columns=['Free Space 1', 'Free Space 2', 'Free Space 3', 'Free Space 4'], inplace=True)
    #print(states_df.dtypes)
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
    cluster_failure_track_vector = []
    #check if any simulations contain errors, remove those simulations
    simulation_start_index = 0
    simulation_end_index = 0
    simulations_to_flush = [] #list of pairs containing [simulation_start_index, simulation_end_index]
    simulation_number = -1
    current_sim_error = False #keeps track if the current sim has errors
    initial_failures_to_pop = []
    for index, row in states_df.iterrows():
        steady_state = row['Steady State'].astype(int)
        line_failure_index = row['Failed Line Index'].astype(int)
        if start_detect == 1: #if previous state was steady state
            simulation_number += 1 #increment the simulation number
            simulation_start_index = index #set the new simulation start index to the current index
            if steady_state != -1: #if this is not a steady state, do not reset the next iteration
                start_detect = 0 #set start_detect to 0
                #simulation_end_index = index #set simulation end index so that it can be flushed
                #simulations_to_flush.append([simulation_start_index, simulation_end_index])
        else: #if previous state was not steady state
            if line_failure_index > number_of_lines:
                #print("ERROR: branch failure not accounted for in cluster. Flushing simulation from dataframe. Index is ", index, "Simulation is ", simulation_number)
                #remove the initial failures vector from the table
                initial_failures_to_pop.append(simulation_number)
                
                #redo this, keep track of initial failures to pop, then do afterword
                current_sim_error = True
            if steady_state == -1: #if steady state, set restart variable to 1
                start_detect = 1
                simulation_end_index = index
                if current_sim_error:
                    num_errors += 1
                    #print("Dropping simulation starting at index ", simulation_start_index, " ending at index ", simulation_end_index)
                    simulations_to_flush.append([simulation_start_index, simulation_end_index]) #add to list to be flushed
                    current_sim_error = False #reset sim_error variable
    #print("Number of simulations: ", simulation_number + 1)
    #print("Initial Failures tracked: ", len(initial_failures))
    
        
    #flush bad simulations from dataframe
    #print("Length of states_df before flushing: ", len(states_df))
    #go through in reverse to keep indeces together
    for simulation in reversed(initial_failures_to_pop):
        print("Initial failures removed: ", initial_failures.pop(simulation)) #remove the initial failures for this simulation
    for entry in reversed(simulations_to_flush):
        #print("Dropping simulation")
        print(states_df.index[entry[0] : entry[1] + 1])
        states_df.drop(states_df.index[entry[0] : entry[1] + 1], inplace=True)
        #states_df.drop(labels = list(range(entry[0], entry[1] + 1)))
    #print("Length of states_df after flushing: ", len(states_df))
    #print(states_df['Steady State'].value_counts())
    #reset indeces
    states_df.reset_index(inplace = True)
    start_detect = 1
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
            
            initial_cluster_failures = []
            for failure in initial_failures[iteration_track]:
                print("Specific failure:", failure)
                for i in range(len(clusters)):
                    if failure in clusters[i]: #if line failure is in cluster i
                        line_failure_row[i] = line_failure_row[i]+1
                        initial_cluster_failures.append(i)
            cluster_failure_track_vector.append(initial_cluster_failures) #append the initial failures vector to the cluster_failure_track vector
            iteration_track = iteration_track+1 #increment iteration tracker -- this iteration is now complete
        else: #if previous state was not steady state
            if steady_state == -1: #if steady state, set restart variable to 1
                start_detect = 1
            test_if_in_failure_index_in_cluster = False
            for i in range(len(clusters)):
                if line_failure_index in clusters[i]: #if line failure is in cluster i
                    #print("Incrementing cluster ", i)
                    line_failure_row[i] = line_failure_row[i]+1
                    temp_cluster_failure_vec = cluster_failure_track_vector[-1] + [] #Get last vector in list of vectors
                    temp_cluster_failure_vec.append(i) #append the region of this failure to that list
                    cluster_failure_track_vector.append(temp_cluster_failure_vec) #append the cluster of the failure to the vector
                    test_if_in_failure_index_in_cluster = True
            #if not test_if_in_failure_index_in_cluster:
                #print("ERROR: branch failure not accounted for in cluster. This could cause unexpected results. Line failure Index is: ", line_failure_index,
                    #" and total number of failures for this state is: ", total_line_failures)

        cluster_failures.append(line_failure_row + []) #append line_failure_row to the cluster_failures list of lists (matrix to be added) -- fix -- add empty list?
        topological_factor_row = [cluster_failure / total_line_failures for cluster_failure in line_failure_row] #create the topological factor row
        print(topological_factor_row)
        cluster_failures_topological_factors.append(topological_factor_row)
    #print(cluster_failures)
    #print(iteration_track)
    #Append region puredata to dataframe

    for i in range(len(clusters)):
        region_df_entry_name = 'Region ' + str(i) + ' Failures'
        region_failure_data = [val[i] for val in cluster_failures]
        #print(region_failure_data)
        states_df[region_df_entry_name] = region_failure_data
    #append topological factor to df
    for i in range(len(clusters)):
        region_df_entry_name = 'Region ' + str(i) + ' Topological Factor'
        region_failure_data = [val[i] for val in cluster_failures_topological_factors]
        #print(region_failure_data)
        states_df[region_df_entry_name] = region_failure_data

    #NEW AS OF OCTOBER 2021: calculate mean and variance
    mean_list = []
    var_list = []
    #calculate mean and var off of cluster_failures_topological factors
    for entry in cluster_failures_topological_factors:
        mean = sum([i * entry[i] for i in range(len(entry))]) #calculate pmf mean
        var = sum([i **2 * entry[i] for i in range(len(entry))]) - mean**2 #calculate pmf variance
        mean_list.append(mean)
        var_list.append(var)
    #add mean and variance entries to the df
    mean_df_name = 'Mean of T'
    var_df_name = 'Variance of T'
    states_df[mean_df_name] = mean_list
    states_df[var_df_name] = var_list
    
    #append the region of failure data
    region_df_entry_name = 'Region of Failure'
    states_df[region_df_entry_name] = cluster_failure_track_vector

    #Save the dataframe
    if save_as_csv:
        if output_df_name[-4:-1] != ['.','c','s','v']:
            output_df_name += '.csv'
        states_df.to_csv(output_df_name, index=False)
        #print("Iteration track = ", iteration_track) #check, should be the number of iterations run
        #print(cluster_failures)
        #print(cluster_failures_topological_factors)
        #if simplifying dataframe, drop unecessary columns
        if use_simplified_df == True:
            states_df.drop(columns=['Maximum failed line capacity', 
                'Load shed from previous step', 'Difference in Load Shed', 
                'Load', 'Capacity of Failed Ones', 'Capacity of Failed Ones 2','Failed Line Index', 
                'Capacity of Failed One', 'Time of Failure Event', 'Demand-Loadshed Difference',
                'Generation'], inplace=True)
        states_df.to_csv(output_df_name, index=False)
        
    print('The number of dropped simulations is: ', str(num_errors))

    return states_df