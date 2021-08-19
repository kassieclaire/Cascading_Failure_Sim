#pmf_dictionary -- each key is a raw topological variable (not normalized), and the vector is a PMF for that raw topological variable
#result_in_new_failure -- a list of length 2, where index 0 counts how many times a failure occurs after the raw topological variable, and index 1 counts how many times this topological variable results in a steady state
#occurence_floor -- set to 1 by default, the number of times that a failure has to occur after this raw topological variable for it to be considered in the trimmed pmf
def trim_steady_regions(pmf_dictionary, result_in_new_failure, occurrence_floor = 1):
    new_result_in_new_failure = result_in_new_failure.copy()
    for key in result_in_new_failure:
        if result_in_new_failure[key][0] < occurrence_floor: #if new line failure never occurred after this region key
            del pmf_dictionary[key] #delete this key from the PMF -- not useful for the PMF
            del new_result_in_new_failure[key]
    return pmf_dictionary, new_result_in_new_failure