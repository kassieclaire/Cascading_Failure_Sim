import pandas as pd
import numpy as np
import scipy.io
def calculate_mean_and_variance(states_matrix, initial_failures, cluster_info):

    ##cluster load code
    cluster_mat = scipy.io.loadmat(cluster_info)
    cluster_lists = [l.tolist() for l in cluster_mat[cluster_info][0]]
    clusters = [[item for sublist in cluster_list for item in sublist] for cluster_list in cluster_lists]

    ##states matrix load code
    mat = scipy.io.loadmat(states_matrix) #the states matrix input -- temporary
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
    states_df.drop(columns=['Free Space 1', 'Free Space 2', 'Free Space 3', 'Free Space 4'], inplace=True)

    ##initial failures load code
    initial_failures_mat = scipy.io.loadmat(initial_failures) #cell of arrays containing the initial failures for each iteration
    initial_failures_arrays = [l.tolist() for l in initial_failures_mat['Initial_Failure_Table']]
    initial_failures = [l.tolist()[0] for l in initial_failures_arrays[0]] #change initial failure matrix into list of lists

    ##region failure tracking code (adds vector to dataframe)
    cluster_failures = []
    cluster_failures_topological_factors = []
    #original values
    start_detect = 1
    line_failure_row = [0]*len(clusters) # set line_failure_row outside since it needs to be kept between iterations
    iteration_track = 0
    cluster_failure_track_vector = []
    mu_vector = []
    variance_vector = []
    #Loop through each index, provide vector
    for index, row in states_df.iterrows():
        steady_state = row['Steady State'].astype(int)
        total_line_failures = row['Total Line Failures'].astype(int)
        line_failure_index = row['Failed Line Index'].astype(int)
        if start_detect == 1: #if previous state was steady state
            if steady_state != -1: #if this is not a steady state, do not reset the next iteration
                start_detect = 0 #set start_detect to 0
            #reset the line failures and then do the for loop for adding for the initial failure
            line_failure_row = [0]*len(clusters)
            
            initial_cluster_failures = []
            for failure in initial_failures[iteration_track]:
                for i in range(len(clusters)):
                    if failure in clusters[i]: #if line failure is in cluster i
                        line_failure_row[i] = line_failure_row[i]+1
                        initial_cluster_failures.append(i)
            cluster_failure_track_vector.append(initial_cluster_failures) #append the initial failures vector to the cluster_failure_track vector
            #NEW: get mean and variance of temp_cluster_failure_vec
            mu = np.mean(initial_cluster_failures)
            variance = np.var(initial_cluster_failures)
            mu_vector.append(mu)
            variance_vector.append(variance)
            #End of new code
            iteration_track = iteration_track+1 #increment iteration tracker -- this iteration is now complete
        else: #if previous state was not steady state
            if steady_state == -1: #if steady state, set restart variable to 1
                start_detect = 1
            test_if_in_failure_index_in_cluster = False
            for i in range(len(clusters)):
                if line_failure_index in clusters[i]: #if line failure is in cluster i
                    line_failure_row[i] = line_failure_row[i]+1
                    temp_cluster_failure_vec = cluster_failure_track_vector[-1] + [] #Get last vector in list of vectors
                    temp_cluster_failure_vec.append(i) #append the region of this failure to that list
                    cluster_failure_track_vector.append(temp_cluster_failure_vec) #append the cluster of the failure to the vector
                    #NEW: get mean and variance of temp_cluster_failure_vec
                    mu = np.mean(temp_cluster_failure_vec)
                    variance = np.var(temp_cluster_failure_vec)
                    mu_vector.append(mu)
                    variance_vector.append(variance)
                    #End of new code
                    test_if_in_failure_index_in_cluster = True
            #Error checking -- if line index not in a defined cluster (happens if simulation's index values include unexpected values)
            if not test_if_in_failure_index_in_cluster:
                print("ERROR: branch failure not accounted for in cluster. This could cause unexpected results. Line failure Index is: ", line_failure_index,
                    " and total number of failures for this state is: ", total_line_failures)

        cluster_failures.append(line_failure_row + []) #append line_failure_row to the cluster_failures list of lists (matrix to be added) -- fix -- add empty list?
        topological_factor_row = [cluster_failure / total_line_failures for cluster_failure in line_failure_row] #create the topological factor row
        cluster_failures_topological_factors.append(topological_factor_row)
    
    ##Form the dataframe
    for i in range(len(clusters)):
        region_df_entry_name = 'Region ' + str(i) + ' Failures'
        region_failure_data = [val[i] for val in cluster_failures]
        states_df[region_df_entry_name] = region_failure_data
    #append topological factor to df
    for i in range(len(clusters)):
        region_df_entry_name = 'Region ' + str(i) + ' Topological Factor'
        region_failure_data = [val[i] for val in cluster_failures_topological_factors]
        states_df[region_df_entry_name] = region_failure_data
    #append the region of failure data
    region_df_entry_name = 'Region of Failure'
    states_df[region_df_entry_name] = cluster_failure_track_vector
    #NEW: append mean and variance
    #mean
    mean_df_entry_name = 'Mean of T'
    states_df[mean_df_entry_name] = mu_vector
    #variance
    variance_df_entry_name = 'Variance of T'
    states_df[variance_df_entry_name] = variance_vector
    #End of new code
    #Save the dataframe
    states_df.to_csv(r'states_dataframe.csv', index=False)

    ##Simplified dataframe generation for easy presentation of resultant information:
    states_simple_df = states_df.copy()
    states_simple_df.drop(columns=['Maximum failed line capacity', 
        'Load shed from previous step', 'Difference in Load Shed', 
        'Load', 'Capacity of Failed Ones', 'Capacity of Failed Ones 2','Failed Line Index', 
        'Capacity of Failed One', 'Time of Failure Event', 'Demand-Loadshed Difference',
        'Generation'], inplace=True)
    states_simple_df.to_csv(r'states_simple.csv', index=False)