from matplotlib.pyplot import plot
from generate_states_dataframe_fixed import generate_states_df
from plot_cascade_stop import plot_p_stop
from pStop_Generic import generate_generic_pStop
import pandas as pd
matrix_directory = 'states_matrices'
cluster_matrix_name = 'cluster_branch_118'
states_matrix_name = 'case118_i1000_f5_r9_t0_e4_sm'
initial_failure_table_name = 'case118_i1000_f5_r9_t0_e4_if'
output_df_name = states_matrix_name + '_df'
number_of_lines = 186
states_df = generate_states_df(clusters_matrix_name=cluster_matrix_name, states_matrix_name=states_matrix_name, initial_failure_table_name=initial_failure_table_name, number_of_lines=number_of_lines, output_df_name=output_df_name)
p_stop_df = generate_generic_pStop(states_df = states_df, variable_name='Total Line Failures')
plot_p_stop(p_stop_df=p_stop_df, variable_name='Total Line Failures')