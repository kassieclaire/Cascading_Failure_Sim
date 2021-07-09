from cascading_failure_function import cascading_failure_function

#Run cascading_failure_function
# Default Inputs: 
# cascading_failure_function(states_matrix_name='states',initial_failure_table_name='initial_failures', 
#   clusters_matrix_name='case_118_clusters', number_of_lines=186, graph_pstop_simple=True, 
#       calculate_region_failure_probabilities=True)
#Input descriptions:
#states_matrix_name :   The name of the .mat states matrix provided by the simulation
#initial_failure_table_name :   The name of the .mat initial failures file provided by the simulation
#clusters_matrix_name   :   The name of the .mat clusters file provided by the clustering function, 
#   should be clusters of branches
#number_of_lines    :   should be the number of lines in the case -- this is approximately equivalent to the number of branches
#graph_pstop_simple :   Whether the typical cascading failure graph should be provided by the function -- set to True to show
#   cascading failure pstop curve based on number of line failures only
#calculate_region_failure_probabilities :   The function will print out the probabilities of a failure occuring in each region
#   assuming that a failures DOES OCCUR. Can be modified to remove this assumption

cascading_failure_function()
