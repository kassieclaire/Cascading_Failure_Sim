import pandas as pd
import numpy as np
import scipy.io
import matplotlib.pyplot as plt
#DONE: TODO: Add probabilities for failure in specific regions based on distribution of current failures in regions
#DONE: TODO: Cluster lines based on bus clusters
#Talk to Brad or Matt to get into workstation, get IP address of workstation in lab -- ask Jamir
#TODO: probability mass distribution given fixed number of failures -- with Jamir/AJ
def cascading_failure_function(states_matrix_name='states',initial_failure_table_name='initial_failures', clusters_matrix_name='case_118_clusters', number_of_lines=186, graph_pstop_simple=True, calculate_region_failure_probabilities=True, use_test_cluster=False):
    
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
            if not test_if_in_failure_index_in_cluster:
                print("ERROR: branch failure not accounted for in cluster. This could cause unexpected results. Line failure Index is: ", line_failure_index,
                    " and total number of failures for this state is: ", total_line_failures)

        cluster_failures.append(line_failure_row + []) #append line_failure_row to the cluster_failures list of lists (matrix to be added) -- fix -- add empty list?
        topological_factor_row = [cluster_failure / total_line_failures for cluster_failure in line_failure_row] #create the topological factor row
        cluster_failures_topological_factors.append(topological_factor_row)
    print(len(cluster_failure_track_vector))
    print(len(states_df.index))
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
    #append the region of failure data
    region_df_entry_name = 'Region of Failure'
    states_df[region_df_entry_name] = cluster_failure_track_vector

    #Save the dataframe
    states_df.to_csv(r'states_dataframe.csv', index=False)
    #print("Iteration track = ", iteration_track) #check, should be the number of iterations run
    #print(cluster_failures)
    #print(cluster_failures_topological_factors)
    states_simple_df = states_df.copy()
    states_simple_df.drop(columns=['Maximum failed line capacity', 
        'Load shed from previous step', 'Difference in Load Shed', 
        'Load', 'Capacity of Failed Ones', 'Capacity of Failed Ones 2','Failed Line Index', 
        'Capacity of Failed One', 'Time of Failure Event', 'Demand-Loadshed Difference',
        'Generation'], inplace=True)
    states_simple_df.to_csv(r'states_simple.csv', index=False)

    cluster_line_failure_df = pd.DataFrame()
    #print(states_df['Total Line Failures'])
    ##REGION PMF FUNCTIONS
    if (calculate_region_failure_probabilities):
        #Format: dataframe consisting of failures in each region, then likelihood of failures for each region (region*2 columns, region combinations visited rows)
        #TODO: Got through the dataframe, find every distinct combination of region failures
        distinct_region_failure_combinations = []
        previous_region_combination = []
        region_failures_after = {}
        new_cascade = True
        for index, row in states_df.iterrows():
            region_combination = []
            #create the region combination
            for i in range(len(clusters)):
                column_name = 'Region ' + str(i) + ' Failures'
                region_combination.append(row[column_name])
            #convert to tuple
            region_combination_key = tuple(region_combination)
            #use as key in dictionary
            if region_combination_key not in region_failures_after:
                #add the key
                region_failures_after[region_combination_key] = [0]*(len(clusters)+1) #add 1 for the probability of not failing
            #if (index != 0 and row['Steady State'] != -1): #if this is not the initial row and not initial failures
            if not new_cascade:
                previous_region_combination_key = tuple(previous_region_combination)
                previous_region_combination = region_combination #set this region combination to the previous for the next iteration
                region_failures_after[previous_region_combination_key][row['Region of Failure'][-1]] += 1 #increment the times in a region that this failure occurs by 1
                if row['Steady State'] == -1:
                    new_cascade = True #next row is new cascade
            elif (index != 0):
                previous_region_combination_key = tuple(previous_region_combination)
                previous_region_combination = region_combination #set this region combination to the previous for the next iteration
                region_failures_after[previous_region_combination_key][-1] += 1 #increment the times a steady state occurs by 1
                if row['Steady State'] != -1:
                    new_cascade = False
            else:
                previous_region_combination = region_combination
                if row['Steady State'] != -1:
                    new_cascade = False
            #see if region combination has occured before
            #if region_combination not in distinct_region_failure_combinations:
                #distinct_region_failure_combinations.append(region_combination)
        print(region_failures_after)
        region_failures_after_normalized = {}
        for key in region_failures_after.keys():
            if (sum(region_failures_after[key]) != 0):
                region_failures_after_normalized[key] = [float(i)/sum(region_failures_after[key]) for i in region_failures_after[key]] #normalize entries
            else:
                region_failures_after_normalized[key] = region_failures_after[key]
        #print(region_failures_after_normalized) #print the dictionary of failures
        #print formatted (code from https://stackoverflow.com/questions/20181899/how-to-make-each-key-value-of-a-dictionary-print-on-a-new-line/20182376)
        print("\n".join("{!r} : {!r}".format(k, v) for k, v in region_failures_after_normalized.items()))


            
        #print(distinct_region_failure_combinations) #test -- print the distinct region failure combinations
        #TODO: calculate likelihood of failure in next region

    ##Cascading Failure Curve Code
    if (graph_pstop_simple):
        total_states = [0] * (number_of_lines + 1)
        stable_states = [0] * (number_of_lines + 1)
        for index, row in states_df.iterrows():
            #print(row['Total Line Failures'])
            total_line_failures = row['Total Line Failures']
            steady_state = row['Steady State']
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