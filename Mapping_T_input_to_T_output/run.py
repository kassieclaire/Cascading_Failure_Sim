from calculate_mean_and_variance import calculate_mean_and_variance
from curve_fit_mu_and_var import curve_fit_mu_and_var
from generate_pmf import generate_pmf
from trim_steady_regions import trim_steady_regions
from cascading_failure_function import cascading_failure_function
from normalize_pmf_keys import normalize_pmf_keys
import pandas as pd
df_name = 'test_df'
mu_and_var_df_name = 'mean_and_variance.csv'
cascading_failure_function(clusters_matrix_name='cluster_branch_39', output_df_name=df_name, use_simplified_df=True, states_matrix_name='case39_initial_failures_count_2_sm', initial_failure_table_name='case39_initial_failures_count_2_if', graph_pstop_simple=False)
(region_failure_pmf, result_in_new_failure) = generate_pmf(df_name)
(trimmed_region_failure_pmf, trimmed_steady_state_track) = trim_steady_regions(region_failure_pmf, result_in_new_failure, occurrence_floor=5)
(normalized_pmf, normalized_steady_state_track) = normalize_pmf_keys(trimmed_region_failure_pmf, trimmed_steady_state_track, debug=True)
mu_and_var = calculate_mean_and_variance(normalized_pmf, normalized_steady_state_track)
print(mu_and_var)
#mu_and_var_df = pd.DataFrame.from_dict(mu_and_var)
#mu_and_var_df.to_csv(mu_and_var_df_name, index=False)
#print(trimmed_region_failure_pmf)
#mu_and_var = calculate_mean_and_variance(trimmed_region_failure_pmf)

