from numpy import sort
import pandas as pd
import matplotlib.pyplot as plt
from statistics import mean, median
from scipy.stats import pearsonr
#DONE: TODO: binary approximation of Cmax (small, large), systematically say where CMax matters, where it doesn't matter
#TODO: check pstop curves, find out what's going on -- talk to Rezoan
#TODO: Lookup table maybe for implementation into state matrix?
#DONE: TODO: generate 2 clusters -- little cmax, large cmax -- look at pmf variance, mean as outputs
#DONE: TODO: aggregate over F -- dropping F from the equation
#DONE: TODO: Make scattergrams
#DONE: TODO: At least 6 plots
#NOTE: Maybe binarization/reduction (tiny/medium/large) of variance?
#NOTE: eventually test the reduced model against a non-reduced model to prove its usefulness if we go in that direction
#NOTE: Jamir's paper -- proofread abstract, introduction, conclusions -- maybe more
#E.g.: When capacity is big.. this is what happens -- likely to be among these clusters -- hence this is happening, etc.
#NOTE: make 1 slide on the user interface for the power grid -- high-level stuff -- TOP PRIORITY
#NOTE: Include pictures of all team members
#Output: tool that makes research accessible to operators, analysts
#Create one slide and send to Dr. Hayat
#Big/small capacity can shed light on what cluster
#for graphing mean instead of variance, set the following to true
#NOTE: Show dramatic event that happens, here's the outcome
#NOTE: Ukraine cyberattacks powergrid blackout -- 2015

normalize_across_F = True
#number of points needed for graphing for particular F, mu, var combination
cutoff = 5
#counter for number of F, mu, var combinations that meet the cutoff
meets_cutoff_counter = 0
#import the mean and variance dataframe
df = pd.read_csv('mean_and_variance.csv')
#find unique F values and iterate through these
failure_vals = df["F"].unique()
if normalize_across_F:
    print('Normalized across F')
    #find unique input means, iterate through these
    mean_vals = df['mu_i'].unique()
    for mu in mean_vals:
        #get the df for only this failure value and mean
        separated_by_f_and_mu_df = df[df['mu_i'] == mu]
        #find unique input variances for that F and mean and iterate through these
        var_vals = separated_by_f_and_mu_df['var_i'].unique()
        for var in var_vals:
            #get the df for only this failure value, mean, and variance
            separated_by_f_mu_and_var_df = separated_by_f_and_mu_df[separated_by_f_and_mu_df['var_i'] == var]
            #print the unique Cmax values
            cmax_vals = separated_by_f_mu_and_var_df['Cmax'].unique()
            if (len(cmax_vals) > cutoff):
                #sort the cmax vals in increasing order
                cmax_vals.sort()
                cmax_median = median(cmax_vals)
                #now, for each cmax value, get the mean of the pmf variances
                cmax_list = []
                mu_o_averaged_list_less = []
                mu_o_averaged_list_more = []
                var_o_averaged_list_less = []
                var_o_averaged_list_more = []
                #go through each cmax
                for cmax in cmax_vals:
                    #append the cmax to a list to keep track of which cmax goes with the averaged var_o
                    cmax_list.append(cmax)
                    #get the df for only this failure value, mean, variance, and cmax
                    separated_by_f_mu_var_and_cmax_df = separated_by_f_mu_and_var_df[separated_by_f_mu_and_var_df['Cmax'] == cmax]
                    #append the averaged mean_o to the mean_o_averaged_list
                    #choose which of the 2 lists to add the value to
                    if cmax <= cmax_median:
                        mu_o_averaged_list_less.append(mean(separated_by_f_mu_var_and_cmax_df['mu_o']))
                        var_o_averaged_list_less.append(mean(separated_by_f_mu_var_and_cmax_df['var_o']))
                    else:
                        mu_o_averaged_list_more.append(mean(separated_by_f_mu_var_and_cmax_df['mu_o']))
                        var_o_averaged_list_more.append(mean(separated_by_f_mu_var_and_cmax_df['var_o']))
                #graph the cmax versus the pmf variance averaged
                fig = plt.figure()
                ax1 = fig.add_subplot(111)
                #create label names
                title = 'Scatterplot showing pmf mean, variance clusters based on CMax for mean = ' +  str(mu) + ", \n and variance = " + str(var)
                label_1 = 'Cmax less than or equal to ' + str(cmax_median)
                label_2 = 'Cmax greater than ' + str(cmax_median)
                #plot the points for less than
                ax1.scatter(mu_o_averaged_list_less, var_o_averaged_list_less, s=10, c='b', marker="s", label=label_1)
                #plot the points for more than
                ax1.scatter(mu_o_averaged_list_more,var_o_averaged_list_more, s=10, c='r', marker="o", label=label_2)
                #add legend
                plt.legend(loc='upper left')
                #add title
                plt.title(title)
                #add labels
                plt.xlabel('Mean of output PMF')
                plt.ylabel('Variance of output PMF')
                plt.show()               
            
else:
    for f in failure_vals:
        #get the df for only this failure value
        separated_by_f_df = df[df['F'] == f]
        #find unique input means for that F and iterate through these
        mean_vals = separated_by_f_df['mu_i'].unique()
        
        #find unique input means for that F and iterate through these
        mean_vals = separated_by_f_df['mu_i'].unique()
        for mu in mean_vals:
            #get the df for only this failure value and mean
            separated_by_f_and_mu_df = separated_by_f_df[separated_by_f_df['mu_i'] == mu]
            #find unique input variances for that F and mean and iterate through these
            var_vals = separated_by_f_and_mu_df['var_i'].unique()
            for var in var_vals:
                #get the df for only this failure value, mean, and variance
                separated_by_f_mu_and_var_df = separated_by_f_and_mu_df[separated_by_f_and_mu_df['var_i'] == var]
                #print the unique Cmax values
                cmax_vals = separated_by_f_mu_and_var_df['Cmax'].unique()
                if (len(cmax_vals) > cutoff):
                    #sort the cmax vals in increasing order
                    cmax_vals.sort()
                    cmax_median = median(cmax_vals)
                    #now, for each cmax value, get the mean of the pmf variances
                    cmax_list = []
                    mu_o_averaged_list_less = []
                    mu_o_averaged_list_more = []
                    var_o_averaged_list_less = []
                    var_o_averaged_list_more = []
                    #go through each cmax
                    for cmax in cmax_vals:
                        #append the cmax to a list to keep track of which cmax goes with the averaged var_o
                        cmax_list.append(cmax)
                        #get the df for only this failure value, mean, variance, and cmax
                        separated_by_f_mu_var_and_cmax_df = separated_by_f_mu_and_var_df[separated_by_f_mu_and_var_df['Cmax'] == cmax]
                        #append the averaged mean_o to the mean_o_averaged_list
                        #choose which of the 2 lists to add the value to
                        if cmax <= cmax_median:
                            mu_o_averaged_list_less.append(mean(separated_by_f_mu_var_and_cmax_df['mu_o']))
                            var_o_averaged_list_less.append(mean(separated_by_f_mu_var_and_cmax_df['var_o']))
                        else:
                            mu_o_averaged_list_more.append(mean(separated_by_f_mu_var_and_cmax_df['mu_o']))
                            var_o_averaged_list_more.append(mean(separated_by_f_mu_var_and_cmax_df['var_o']))
                    #graph the cmax versus the pmf variance averaged
                    fig = plt.figure()
                    ax1 = fig.add_subplot(111)
                    #create label names
                    title = 'Scatterplot showing pmf mean, variance clusters based on CMax for f = ' + str(f) + ", mean = " +  str(mu) + ", \n and variance = " + str(var)
                    label_1 = 'Cmax less than or equal to ' + str(cmax_median)
                    label_2 = 'Cmax greater than ' + str(cmax_median)
                    #plot the points for less than
                    ax1.scatter(mu_o_averaged_list_less, var_o_averaged_list_less, s=10, c='b', marker="s", label=label_1)
                    #plot the points for more than
                    ax1.scatter(mu_o_averaged_list_more,var_o_averaged_list_more, s=10, c='r', marker="o", label=label_2)
                    #add legend
                    plt.legend(loc='upper left')
                    #add title
                    plt.title(title)
                    #add labels
                    plt.xlabel('Mean of output PMF')
                    plt.ylabel('Variance of output PMF')
                    plt.show()               
                    

                    