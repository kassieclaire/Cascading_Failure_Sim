from re import A
from calculate_mean_and_variance import calculate_mean_and_variance
from calculate_mean_and_variance_with_c import calculate_mean_and_variance_with_c
from curve_fit_mu_and_var import curve_fit_mu_and_var
from generate_pmf import generate_pmf
from generate_pmf_with_failure_count import generate_pmf_with_failure_count
from generate_pmf_with_failure_count_and_max_cap import generate_pmf_with_failure_count_and_cap
from trim_steady_regions import trim_steady_regions
from cascading_failure_function import cascading_failure_function
from normalize_pmf_keys import normalize_pmf_keys
from generate_states_dataframe_fixed import generate_states_df
import os, sys
#from separate_by_F import separate_by_F
#NOTE: keep track of F and separate F's
import pandas as pd
#number_of_line_failures = 2 #specify number of failures to look for
state_matrix_name = 'case39_initial_failures_count_2_sm'
initial_failure_table_name = 'case39_initial_failures_count_2_if'
df_name = 'test_df'
mu_and_var_df_name = 'mean_and_variance.csv'
number_of_lines = 46
occurrence_floor = 5


number_of_line_failures_list = list(range(2,46))
############################################################################################################
#CHANGE THIS FOR RUNS
line_failure_counts_list = [[2, 220], [3, 100], [7, 300]] #initial line failure counts for simulation groups
run_df_generation = False #to generate new data, set to true
use_max_cap = True #to test with max cap on top of line failures -- to see if max cap impacts pmf -- set to true
############################################################################################################

num_sims_list = list(range(1,221))
#go through multiple matrices, transform them into dataframes and combine them

if run_df_generation:
    combined_states_df = generate_states_df(number_of_lines=number_of_lines, clusters_matrix_name='cluster_branch_39', output_df_name=df_name, use_simplified_df=True, states_matrix_name=state_matrix_name, initial_failure_table_name=initial_failure_table_name)
    for line_failure_count_and_iterations in line_failure_counts_list:
        line_failure_count = line_failure_count_and_iterations[0]
        num_sims_list = list(range(1, line_failure_count_and_iterations[1]+1))
        folder_name = "F_" + str(line_failure_count) + "_IEEE_39"
        for iteration in num_sims_list:
            state_matrix_name = "states_IEEE39_F_" + str(line_failure_count) + "_" + str(iteration)
            initial_failure_table_name =  "initial_failures_IEEE39_F_" + str(line_failure_count) + "_" + str(iteration)
            temp_df = generate_states_df(number_of_lines=number_of_lines,clusters_matrix_name='cluster_branch_39', output_df_name=df_name, use_simplified_df=True, states_matrix_name=state_matrix_name, initial_failure_table_name=initial_failure_table_name, states_matrix_folder=folder_name)
            combined_states_df.append(temp_df) #append this on
    combined_states_df.to_csv(df_name + ".csv", index=False)
#go back up 
path_parent = os.path.dirname(os.getcwd())

#unique_caps = combined_states_df["Capacity of Failed One"].unique()

if use_max_cap:
    #do this
    (region_failure_pmf, result_in_new_failure) = generate_pmf_with_failure_count_and_cap(df_name)
    #c_separated_pmf = [{} for _ in unique_caps]
    f_and_c_separated_pmf = [{} for _ in range(number_of_lines)]
    f_and_c_separated_failure_tracker = [{} for _ in range(number_of_lines)]
    for key in region_failure_pmf:
        num_failures = sum(list(key)[0:-1])#grab number of failures -- changed -- don't include last in list, that's max cap
        max_cap = list(key)[-1] #grab max cap
        #print(max_cap) #TEMP
        #Edit: wasn't figuring out the key right
        if (sum(region_failure_pmf[key]) != 0):
            pmf = region_failure_pmf[key] #grab all values minus the last (number of line failures)
            tracker = result_in_new_failure[key]
            #CHANGE: still have the normalized key, but then add extra value (cmax) to it
            #normalized_key = tuple([float(i)/sum(list(key)[0:-1]) for i in list(key)[0:-1]]) #changed to cut off the last value
            #print(sum(list(key)[0:-1]))
            if (sum(list(key)[0:-1]) > 0):
                normalized_key = [float(i)/sum(list(key)[0:-1]) for i in list(key)[0:-1]] #changed to cut off the last value
            else: # do not normalize if sum is 0
                normalized_key = list(key)[0:-1] #cut off C
            T_C_key = normalized_key #append normalized topological variable to the key (the T)
            T_C_key.append(max_cap) #append maximum capacity to the key (the C)
            T_C_key = tuple(T_C_key)
            f_and_c_separated_pmf[num_failures][T_C_key] = pmf
            f_and_c_separated_failure_tracker[num_failures][T_C_key] = tracker
    #print(f_separated_pmf[number_of_line_failures]) #show the input Ts and output pmfs for 2 line failures



    f_and_c_separated_mu_and_var = [calculate_mean_and_variance_with_c(f_and_c_separated_pmf[i], f_and_c_separated_failure_tracker[i])
        for i in number_of_line_failures_list]
    number_of_failures = []
    number_of_failures = []

    input_mu = []
    output_mu = []
    input_var = []
    output_var = []
    cmax_list = []
    for num_failures in number_of_line_failures_list:
        mu_and_var = f_and_c_separated_mu_and_var[num_failures - number_of_line_failures_list[0]]
        for key in mu_and_var:
            print(key)
            number_of_failures.append(num_failures)
            input_mu_and_var = list(key) #get input mean and variance from key
            input_mu_and_var = input_mu_and_var[0:-1]
            print(input_mu_and_var)
            cmax = list(key)[-1] #grab cmax from end
            cmax_list.append(cmax) #append cmax to the cmax list
            output_mu_and_var = mu_and_var[key]
            input_mu.append(input_mu_and_var[0])
            input_var.append(input_mu_and_var[1])
            output_mu.append(output_mu_and_var[0])
            output_var.append(output_mu_and_var[1])
    mu_and_var_df=pd.DataFrame({'F' : number_of_failures, 'Cmax' : cmax_list, 'mu_i' : input_mu, 'var_i' : input_var, 'mu_o' : output_mu, 'var_o' : output_var})
    print(mu_and_var_df)
    mu_and_var_df.to_csv(mu_and_var_df_name, index=False)

else:
    ##just F separation
    (region_failure_pmf, result_in_new_failure) = generate_pmf_with_failure_count(df_name)
    
    f_separated_pmf = [{} for _ in range(number_of_lines)]
    f_separated_failure_tracker = [{} for _ in range(number_of_lines)]
    for key in region_failure_pmf:
        num_failures = sum(list(key))#grab number of failures
        if (sum(region_failure_pmf[key]) != 0):
            pmf = region_failure_pmf[key] #grab all values minus the last (number of line failures)
            tracker = result_in_new_failure[key]
            normalized_key = tuple([float(i)/sum(list(key)) for i in list(key)])
            f_separated_pmf[num_failures][normalized_key] = pmf
            f_separated_failure_tracker[num_failures][normalized_key] = tracker
    #print(f_separated_pmf[number_of_line_failures]) #show the input Ts and output pmfs for 2 line failures



    f_separated_mu_and_var = [calculate_mean_and_variance(f_separated_pmf[i], f_separated_failure_tracker[i])
        for i in number_of_line_failures_list]
    number_of_failures = []

    input_mu = []
    output_mu = []
    input_var = []
    output_var = []
    for num_failures in number_of_line_failures_list:
        mu_and_var = f_separated_mu_and_var[num_failures - number_of_line_failures_list[0]]
        for key in mu_and_var:
            number_of_failures.append(num_failures)
            input_mu_and_var = list(key)
            output_mu_and_var = mu_and_var[key]
            input_mu.append(input_mu_and_var[0])
            input_var.append(input_mu_and_var[1])
            output_mu.append(output_mu_and_var[0])
            output_var.append(output_mu_and_var[1])
    mu_and_var_df=pd.DataFrame({'F' : number_of_failures, 'mu_i' : input_mu, 'var_i' : input_var, 'mu_o' : output_mu, 'var_o' : output_var})
    print(mu_and_var_df)
    mu_and_var_df.to_csv(mu_and_var_df_name, index=False)

