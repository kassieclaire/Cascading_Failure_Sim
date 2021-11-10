#Function to generate probability mass functions from given state matrix
#Input: state dataframe (csv) with region failures calculated
#Output: Dictionary of tuple region failures as keys and region failure PMFs as mapped values
import pandas as pd
import numpy as np
import ast
#import ast.literal_eval as le
def generate_pmf_with_failure_count(states_df):
    if states_df[-4:-1] != ['.','c','s','v']:
        states_df += '.csv'
    states_df = pd.read_csv(states_df)
    
    #Format: dataframe consisting of failures in each region, then likelihood of failures for each region (region*2 columns, region combinations visited rows)
    #TODO: Got through the dataframe, find every distinct combination of region failures
    previous_region_combination = []
    region_failures_after = {}
    result_in_new_failure = {} #dictionary that keeps count of number of times that this region combination results in a new failure (index 0) and number of times it is a steady state (index 1)
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
        #add on the total number of failures as an identifier to the end
        #region_combination.append(row["Total Line Failures"])
        #convert to tuple
        region_combination_key = tuple(region_combination)
        #use as key in dictionary
        if region_combination_key not in region_failures_after:
            #add the key to the non-normalized pmf dictionary
            region_failures_after[region_combination_key] = [0]*(i) #add 1 for the probability of not failing
            #add the key to the not-stop/stop dictionary
            result_in_new_failure[region_combination_key] = [0, 0]
        #if (index != 0 and row['Steady State'] != -1): #if this is not the initial row and not initial failures
        if not new_cascade:
            previous_region_combination_key = tuple(previous_region_combination)
            previous_region_combination = region_combination #set this region combination to the previous for the next iteration
            regions_of_failure_list = ast.literal_eval(row['Region of Failure'])
            region_failures_after[previous_region_combination_key][regions_of_failure_list[-1]] += 1 #increment the times in a region that this failure occurs by 1
            #increment the number of times that the previous region key results in an extra failure
            result_in_new_failure[previous_region_combination_key][0] += 1
            if row['Steady State'] == -1:
                new_cascade = True #next row is new cascade
        elif (index != 0): #if new cascade
            previous_region_combination_key = tuple(previous_region_combination)
            previous_region_combination = region_combination #set this region combination to the previous for the next iteration
            #region_failures_after[previous_region_combination_key][-1] += 1 #increment the times a steady state occurs by 1 -- (NOT USED -- uncomment if adding last index for keeping track of number of times results in no failure)
            #increment the number of of times that the previous region key results in a steady state
            result_in_new_failure[previous_region_combination_key][1] += 1
            if row['Steady State'] != -1:
                new_cascade = False
        else:
            previous_region_combination = region_combination
            if row['Steady State'] != -1:
                new_cascade = False
        #see if region combination has occured before
        #if region_combination not in distinct_region_failure_combinations:
            #distinct_region_failure_combinations.append(region_combination)
        region_failures_after_normalized = {}
        for key in region_failures_after.keys():
            if (sum(region_failures_after[key]) != 0):
                region_failures_after_normalized[key] = [float(i)/sum(region_failures_after[key]) for i in region_failures_after[key][0:(len(region_failures_after[key]))]] #normalize entries
                #region_failures_after_normalized[key].append(region_failures_after[key][-1])
            else:
                region_failures_after_normalized[key] = region_failures_after[key]
    return region_failures_after_normalized, result_in_new_failure
