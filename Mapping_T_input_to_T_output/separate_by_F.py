def separate_by_F(pmf, steady_state_track, number_of_lines):
    F_separated_pmf = {{} for val in range(number_of_lines)}
    F_separated_steady_state_track = {{}} * number_of_lines
    #Create empty dictionaries for every count of lines reachable
    for key in pmf:
        #calculate the number of failed lines by summing the raw topological input
        number_of_failures = sum(list(key))
        #add this dictionary entry to the specific dictionary
        F_separated_pmf[number_of_failures][key] = pmf[key]
        F_separated_steady_state_track[number_of_failures][key] = steady_state_track[key]
    return F_separated_pmf, F_separated_steady_state_track

