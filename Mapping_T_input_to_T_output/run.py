from calculate_mean_and_variance import calculate_mean_and_variance
from curve_fit_mu_and_var import curve_fit_mu_and_var
from generate_pmf import generate_pmf
from generate_pmf_with_failure_count import generate_pmf_with_failure_count
from trim_steady_regions import trim_steady_regions
from cascading_failure_function import cascading_failure_function
from normalize_pmf_keys import normalize_pmf_keys
#from separate_by_F import separate_by_F
#NOTE: keep track of F and separate F's
import pandas as pd
#
df_name = 'test_df'
mu_and_var_df_name = 'mean_and_variance.csv'
number_of_lines = 46
occurrence_floor = 5
cascading_failure_function(clusters_matrix_name='cluster_branch_39', output_df_name=df_name, use_simplified_df=True, states_matrix_name='case39_initial_failures_count_2_sm', initial_failure_table_name='case39_initial_failures_count_2_if', graph_pstop_simple=False)
#(region_failure_pmf, result_in_new_failure) = generate_pmf(df_name)
(region_failure_pmf, result_in_new_failure) = generate_pmf_with_failure_count(df_name)
#separate failure count from region_failure_pmf and result_in_new_failure
#print(region_failure_pmf)
f_separated_pmf_and_new_failure_tracker = [{} for _ in range(number_of_lines)]
for key in region_failure_pmf:
    num_failures = sum(list(key))#grab number of failures from end
    if (sum(region_failure_pmf[key]) != 0):
        pmf = region_failure_pmf[key] #grab all values minus the last (number of line failures)
        tracker = result_in_new_failure[key]
        normalized_key = tuple([float(i)/sum(list(key)) for i in list(key)])
        print(num_failures)
        #f_separated_pmf_and_new_failure_tracker[num_failures].append([pmf, tracker])
        f_separated_pmf_and_new_failure_tracker[num_failures][normalized_key] = pmf
print(f_separated_pmf_and_new_failure_tracker[2]) #show the input Ts and output pmfs for 2 line failures


#print(region_failure_pmf)
#print(result_in_new_failure)
#(F_categorized_pmf, F_categorized_steady_state_track) = separate_by_F(region_failure_pmf, result_in_new_failure, number_of_lines)
#debug: see if split properly
(trimmed_region_failure_pmf, trimmed_steady_state_track) = trim_steady_regions(region_failure_pmf, result_in_new_failure, occurrence_floor=5)
(normalized_pmf, normalized_steady_state_track) = normalize_pmf_keys(trimmed_region_failure_pmf, trimmed_steady_state_track, debug=True)
mu_and_var = calculate_mean_and_variance(normalized_pmf, normalized_steady_state_track)
#print(mu_and_var)
# print("pmf type (0 deep): ", type(F_categorized_pmf))
# print("Steady state track type (0 deep): ", type(F_categorized_steady_state_track))
# print("pmf type (1 deep): ", type(F_categorized_pmf[3]))
# print("Steady state track type (1 deep): ", type(F_categorized_steady_state_track[3]))
# print(F_categorized_pmf[3])
# F_categorized_normalized_pmf = [{} for val in range(number_of_lines)]
# F_categorized_normalized_steady_state_track = [{} for val in range(number_of_lines)]
# F_categorized_mu_and_var = [{} for val in range(number_of_lines)]
# for i in range(number_of_lines):
# #for i in range(2, 6):
#     (trimmed_region_failure_pmf, trimmed_steady_state_track) = trim_steady_regions(F_categorized_pmf[i], F_categorized_steady_state_track[i], occurrence_floor)
#     (normalized_pmf, normalized_steady_state_track) = normalize_pmf_keys(trimmed_region_failure_pmf, trimmed_steady_state_track, debug=True)
#     mu_and_var = calculate_mean_and_variance(normalized_pmf, normalized_steady_state_track)
#     F_categorized_normalized_pmf[i] = normalized_pmf.copy()
#     F_categorized_normalized_steady_state_track[i] = normalized_steady_state_track.copy()
#     F_categorized_mu_and_var[i] = mu_and_var.copy()
    
# print(F_categorized_normalized_pmf[3])
# print(F_categorized_mu_and_var[3])
#mu_and_var_df = pd.DataFrame.from_dict(mu_and_var)
#mu_and_var_df.to_csv(mu_and_var_df_name, index=False)
#print(trimmed_region_failure_pmf)
#mu_and_var = calculate_mean_and_variance(trimmed_region_failure_pmf)

