from calculate_mean_and_variance import calculate_mean_and_variance
from curve_fit_mu_and_var import curve_fit_mu_and_var
from generate_pmf import generate_pmf
from generate_pmf_with_failure_count import generate_pmf_with_failure_count
from trim_steady_regions import trim_steady_regions
from cascading_failure_function import cascading_failure_function
from normalize_pmf_keys import normalize_pmf_keys
from generate_states_dataframe_fixed import generate_states_df
import os, sys
#from separate_by_F import separate_by_F
#NOTE: keep track of F and separate F's
import pandas as pd
number_of_line_failures = 2 #specify number of failures to look for
go_through_all_matrices = False
state_matrix_name = 'case39_initial_failures_count_2_sm'
initial_failure_table_name = 'case39_initial_failures_count_2_if'
df_name = 'test_df'
mu_and_var_df_name = 'mean_and_variance.csv'
number_of_lines = 46
occurrence_floor = 5
run_df_generation = True

line_failure_counts_list = [2, 3, 7]
num_sims_list = list(range(1,221))
#go through multiple matrices
combined_states_df = generate_states_df(number_of_lines=number_of_lines, clusters_matrix_name='cluster_branch_39', output_df_name=df_name, use_simplified_df=True, states_matrix_name=state_matrix_name, initial_failure_table_name=initial_failure_table_name)
line_failure_count = 2 #temporary, looking only at 2
folder_name = "F_" + str(line_failure_count) + "_IEEE_39"
#folder_name = "F_2_IEEE_39"
#add folder to system path
#sys.path.append(os.path.join(os.path.dirname(__file__), folder_name))
#os.chdir(os.path.join(os.path.dirname(__file__), folder_name))
#print("SYSTEM PATH: ", sys.path)
for iteration in num_sims_list:
    state_matrix_name = "states_IEEE39_F_" + str(line_failure_count) + "_" + str(iteration)
    initial_failure_table_name =  "initial_failures_IEEE39_F_" + str(line_failure_count) + "_" + str(iteration)
    temp_df = generate_states_df(number_of_lines=number_of_lines,clusters_matrix_name='cluster_branch_39', output_df_name=df_name, use_simplified_df=True, states_matrix_name=state_matrix_name, initial_failure_table_name=initial_failure_table_name, states_matrix_folder=folder_name)
    combined_states_df.append(temp_df) #append this on
combined_states_df.to_csv(df_name + ".csv", index=False)
#go back up 
path_parent = os.path.dirname(os.getcwd())
#os.chdir(path_parent)
#print system path again
print("SYSTEM PATH: ", sys.path)
#cascading_failure_function(clusters_matrix_name='cluster_branch_39', output_df_name=df_name, use_simplified_df=True, states_matrix_name=state_matrix_name, initial_failure_table_name=initial_failure_table_name, graph_pstop_simple=False)

#(region_failure_pmf, result_in_new_failure) = generate_pmf(df_name)
(region_failure_pmf, result_in_new_failure) = generate_pmf_with_failure_count(df_name)
#separate failure count from region_failure_pmf and result_in_new_failure
#print(region_failure_pmf)
f_separated_pmf = [{} for _ in range(number_of_lines)]
f_separated_failure_tracker = [{} for _ in range(number_of_lines)]
for key in region_failure_pmf:
    num_failures = sum(list(key))#grab number of failures from end
    if (sum(region_failure_pmf[key]) != 0):
        pmf = region_failure_pmf[key] #grab all values minus the last (number of line failures)
        tracker = result_in_new_failure[key]
        normalized_key = tuple([float(i)/sum(list(key)) for i in list(key)])
        #print(num_failures)
        #f_separated_pmf_and_new_failure_tracker[num_failures].append([pmf, tracker])
        f_separated_pmf[num_failures][normalized_key] = pmf
        f_separated_failure_tracker[num_failures][normalized_key] = tracker
print(f_separated_pmf[number_of_line_failures]) #show the input Ts and output pmfs for 2 line failures


#print(region_failure_pmf)
#print(result_in_new_failure)
#(F_categorized_pmf, F_categorized_steady_state_track) = separate_by_F(region_failure_pmf, result_in_new_failure, number_of_lines)
#debug: see if split properly
#(trimmed_region_failure_pmf, trimmed_steady_state_track) = trim_steady_regions(region_failure_pmf, result_in_new_failure, occurrence_floor=5)
#(normalized_pmf, normalized_steady_state_track) = normalize_pmf_keys(trimmed_region_failure_pmf, trimmed_steady_state_track, debug=True)
mu_and_var = calculate_mean_and_variance(f_separated_pmf[number_of_line_failures], f_separated_failure_tracker[number_of_line_failures])
#print(mu_and_var)
input_mu = []
output_mu = []
input_var = []
output_var = []
for key in mu_and_var:
    input_mu_and_var = list(key)
    output_mu_and_var = mu_and_var[key]
    input_mu.append(input_mu_and_var[0])
    input_var.append(input_mu_and_var[1])
    output_mu.append(output_mu_and_var[0])
    output_var.append(output_mu_and_var[1])
mu_and_var_df=pd.DataFrame({'mu_i' : input_mu, 'var_i' : input_var, 'mu_o' : output_mu, 'var_o' : output_var})
print(mu_and_var_df)
mu_and_var_df.to_csv(mu_and_var_df_name, index=False)

