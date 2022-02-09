import os, sys
import pandas as pd
from F_pStop import generate_F_pStop
from C_pStop import generate_C_pStop
from pStop_Generic import generate_generic_pStop
from plot_cascade_stop import plot_p_stop
from generate_states_dataframe import generate_states_df

os.chdir(os.path.dirname(os.path.realpath(__file__)))
#dir_path = os.getcwd()
matrix_directory = 'states_matrices'
#print(sys.path)
#variables set by user
manually_enter_matrix = False

#variable name can be from this list: ['Total Line Failures', 'Maximum failed line capacity', 
        # 'Load shed from previous step', 'Difference in Load Shed', 
        # 'Load', 'Free Space 1', 'Free Space 2', 'Steady State', 
        # 'Capacity of Failed Ones', 'Capacity of Failed Ones 2', 'Failed Line Index', 
        # 'Capacity of Failed One', 'Time of Failure Event', 
        # 'Accumulation of Failed Capacities', 'Free Space 3', 'Demand-Loadshed Difference',
        # 'Free Space 4', 'Generation']
#variable_name = 'Variance of T'
variable_name = 'Mean of T'
#variable_name = 'Variance of T'
#variable_name = 'Maximum failed line capacity'

states_df = pd.DataFrame
if (manually_enter_matrix):
    for i in range(1,37):
        cluster_matrix_name = 'cluster_branch_39'
        states_matrix_name = 'states_IEEE39_' + str(i)
        initial_failure_table_name = 'initial_failures_IEEE39_' + str(i)
        if states_df.empty:
            states_df = generate_states_df(clusters_matrix_name=cluster_matrix_name, states_matrix_name=states_matrix_name, initial_failure_table_name=initial_failure_table_name, number_of_lines=46)
        else:
            states_df.append(generate_states_df(clusters_matrix_name=cluster_matrix_name, states_matrix_name=states_matrix_name, initial_failure_table_name=initial_failure_table_name, number_of_lines=46))
    states_df.to_csv("Large_states_df.csv", index=False)
else:
    states_df = pd.read_csv("Large_states_df.csv")
    states_df = states_df.astype({'Total Line Failures' : int, 'Maximum failed line capacity' : int, 
        'Load shed from previous step' : float, 'Difference in Load Shed' : float, 
        'Load' : float, 'Steady State' : int, 
        'Capacity of Failed Ones' : float, 'Capacity of Failed Ones 2' : float, 'Failed Line Index' : int, 
        'Capacity of Failed One' : float, 'Time of Failure Event' : float, 
        'Accumulation of Failed Capacities' : int, 'Demand-Loadshed Difference' : float,
        'Generation' : float})

#create p_stop curve
##TEMPORARY CODE FOR SETTING NUMBER OF FAILURES (CURRENTLY SET AT 5)
df_5_failures = states_df[states_df['Total Line Failures'] == 5]
df_5_failures.reset_index(inplace=True)
print(df_5_failures)

##SECTION OF INTEREST
p_stop_df = generate_generic_pStop(states_df = df_5_failures, variable_name = variable_name, amount_to_round = 2) #generate pStop dataframe
#print(p_stop_df) #debugging: print pStop dataframe

#graph the result
plot_p_stop(p_stop_df=p_stop_df, variable_name=variable_name)