#Function to generate probability mass functions from given state matrix
#Input: state dataframe with region failures calculated
#Output: Dictionary of tuple region failures as keys and region failure PMFs as mapped values
import pandas as pd
import numpy as np
def generate_pmf(states_df):
    states_df = pd.read_csv(states_df)
    
    #Format: dataframe consisting of failures in each region, then likelihood of failures for each region (region*2 columns, region combinations visited rows)
    #TODO: Got through the dataframe, find every distinct combination of region failures
    distinct_region_failure_combinations = []
    previous_region_combination = []
    region_failures_after = {}
    new_cascade = True
    for index, row in states_df.iterrows():
        region_combination = []
        #create the region combination
        i = 0
        column_name = 'Region ' + str(i) + ' Failures'
        while set([column_name]).issubset(states_df.columns):
            region_combination.append(row[column_name])
            i = i + 1
            column_name = 'Region ' + str(i) + ' Failures'
        #convert to tuple
        region_combination_key = tuple(region_combination)
        #use as key in dictionary
        if region_combination_key not in region_failures_after:
            #add the key
            region_failures_after[region_combination_key] = [0]*i #add 1 for the probability of not failing
        #if (index != 0 and row['Steady State'] != -1): #if this is not the initial row and not initial failures
        if not new_cascade:
            previous_region_combination_key = tuple(previous_region_combination)
            previous_region_combination = region_combination #set this region combination to the previous for the next iteration
            region_failures_after[previous_region_combination_key][row['Region of Failure'][-1]] += 1 #increment the times in a region that this failure occurs by 1
            if row['Steady State'] == -1:
                new_cascade = True #next row is new cascade
        elif (index != 0):
            previous_region_combination_key = tuple(previous_region_combination)
            previous_region_combination = region_combination #set this region combination to the previous for the next iteration
            region_failures_after[previous_region_combination_key][-1] += 1 #increment the times a steady state occurs by 1
            if row['Steady State'] != -1:
                new_cascade = False
        else:
            previous_region_combination = region_combination
            if row['Steady State'] != -1:
                new_cascade = False
        #see if region combination has occured before
        #if region_combination not in distinct_region_failure_combinations:
            #distinct_region_failure_combinations.append(region_combination)
        print(region_failures_after)
        region_failures_after_normalized = {}
        for key in region_failures_after.keys():
            if (sum(region_failures_after[key]) != 0):
                region_failures_after_normalized[key] = [float(i)/sum(region_failures_after[key]) for i in region_failures_after[key]] #normalize entries
            else:
                region_failures_after_normalized[key] = region_failures_after[key]
    return region_failures_after_normalized
