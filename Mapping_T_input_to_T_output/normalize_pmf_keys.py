def normalize_pmf_keys(pmf, steady_state):
    normalized_pmf = {}
    normalized_steady_state_track = {}
    for key in pmf:
        list_key = list(key)
        normalized_key = tuple([float(i)/sum(list_key) for i in list_key])
        normalized_pmf[normalized_key] = pmf[key]
        normalized_steady_state_track[normalized_key] = steady_state[key]

    return normalized_pmf, normalized_steady_state_track
