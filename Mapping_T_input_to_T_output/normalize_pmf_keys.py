def normalize_pmf_keys(pmf, steady_state, debug = False):
    normalized_pmf = {}
    normalized_steady_state_track = {}
    for key in pmf:
        list_key = list(key)
        normalized_key = tuple([float(i)/sum(list_key) for i in list_key])
        if normalized_key not in normalized_pmf:
            normalized_pmf[normalized_key] = pmf[key]
            normalized_steady_state_track[normalized_key] = steady_state[key]
            #For when keeping track of overlaps matters
            #normalized_pmf[normalized_key] = [pmf[key]]
            #normalized_steady_state_track[normalized_key] = [steady_state[key]]
        else:
            if debug == True:
                print("key overlap!")
            #normalized_pmf[normalized_key].append(pmf[key])
            #normalized_steady_state_track[normalized_key].append(steady_state[key])

    return normalized_pmf, normalized_steady_state_track
