def calculate_mean_and_variance(pmf_dictionary, steady_state_dictionary):
    num_recurring_values = 0 #number of times values overlap, useful for determining if mu and var useful
    mu_and_var = {}
    track_recurring_values = {} #dictionary where "-1" indicates that this value needs to be a weighted mean
    track_concurring_topologies = {} #dictionary of list of lists containing number of non-pstop occurences (index 0) and mapped value tuples (index 1)
    for key in pmf_dictionary:
        #get the values for the key
        key_list = list(key)
        key_mean = sum([(i+1) * key_list[i] for i in range(0, len(key_list))])
        key_var = sum([(i+1)**2 * key_list[i] for i in range(0, len(key_list))]) - key_mean**2
        mean_var_key = (key_mean, key_var)
        #get the values for the mapped value
        mapped_mean = sum([(i+1) * pmf_dictionary[key][i] for i in range(0, len(pmf_dictionary[key]))])
        mapped_var = sum([(i+1)**2 * pmf_dictionary[key][i] for i in range(0, len(pmf_dictionary[key]))]) - mapped_mean**2
        mean_var_mapped_value = [mapped_mean, mapped_var]
        #add the result to the dictionary
        if mean_var_key not in mu_and_var:
            mu_and_var[mean_var_key] = mean_var_mapped_value
            track_concurring_topologies[mean_var_key] = [[steady_state_dictionary[key][0],mean_var_mapped_value]]
        else:
            track_recurring_values[mean_var_key] = -1
            track_concurring_topologies[mean_var_key].append([steady_state_dictionary[key][0], mean_var_mapped_value])
            num_recurring_values += 1
    #now do a weighted mean of the means and variance of recurring values
    for key in track_recurring_values:
        #print(track_concurring_topologies[key])
        occurence_list = [l[0] for l in track_concurring_topologies[key]]
        weighted_mean_of_mapped_mean = 1/(sum(occurence_list))*sum([occurence_list[i]*track_concurring_topologies[key][i][1][0] for i in range(len(track_concurring_topologies[key]))])
        weighted_mean_of_mapped_var = 1/(sum(occurence_list))*sum([occurence_list[i]*track_concurring_topologies[key][i][1][1] for i in range(len(track_concurring_topologies[key]))])
        mean_var_mapped_value = [weighted_mean_of_mapped_mean, weighted_mean_of_mapped_var]
        mu_and_var[key] = mean_var_mapped_value
    print("The number of recurring mean/var input pairs is: ", num_recurring_values)
    return mu_and_var
        