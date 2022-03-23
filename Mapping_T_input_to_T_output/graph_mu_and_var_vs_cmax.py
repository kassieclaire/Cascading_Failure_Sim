from numpy import sort
import pandas as pd
import matplotlib.pyplot as plt
from statistics import mean, median
from scipy.stats import pearsonr
#DONE: TODO: binary approximation of Cmax (small, large), systematically say where CMax matters, where it doesn't matter
#TODO: check pstop curves, find out what's going on -- talk to Rezoan
#TODO: Lookup table maybe for implementation into state matrix?
#TODO: generate 2 clusters -- little cmax, large cmax -- look at pmf variance, mean as outputs
#TODO: aggregate over F -- dropping F from the equation
#TODO: Make scattergrams
#TODO: At least 6 plots
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

graph_mu = False
#Use binary Cmax -- split by median -- below median, above median
binary_C_max = True
#number of points needed for graphing for particular F, mu, var combination
cutoff = 12
#counter for number of F, mu, var combinations that meet the cutoff
meets_cutoff_counter = 0
#import the mean and variance dataframe
df = pd.read_csv('mean_and_variance.csv')
#find unique F values and iterate through these
failure_vals = df["F"].unique()
for f in failure_vals:
    #get the df for only this failure value
    separated_by_f_df = df[df['F'] == f]
    #find unique input means for that F and iterate through these
    mean_vals = separated_by_f_df['mu_i'].unique()
    if binary_C_max:
        if graph_mu:
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
                            else:
                                mu_o_averaged_list_more.append(mean(separated_by_f_mu_var_and_cmax_df['mu_o']))
                        print("For mean, var pair (" + str(mu) + ", " + str(var) + ") " + " and cmax less than or equal to/greater than " + str(cmax_median) + " the average pmf mean is \n(" + str(mean(mu_o_averaged_list_less)) + ", " + str(mean(mu_o_averaged_list_more)) + ")")
        else:
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
                        var_o_averaged_list_less = []
                        var_o_averaged_list_more = []
                        #go through each cmax
                        for cmax in cmax_vals:
                            #append the cmax to a list to keep track of which cmax goes with the averaged var_o
                            cmax_list.append(cmax)
                            #get the df for only this failure value, mean, variance, and cmax
                            separated_by_f_mu_var_and_cmax_df = separated_by_f_mu_and_var_df[separated_by_f_mu_and_var_df['Cmax'] == cmax]
                            #append the averaged var_o to the var_o_averaged_list
                            if cmax <= cmax_median:
                                var_o_averaged_list_less.append(mean(separated_by_f_mu_var_and_cmax_df['var_o']))
                            else:
                                var_o_averaged_list_more.append(mean(separated_by_f_mu_var_and_cmax_df['var_o']))
                        print("For mean, var pair (" + str(mu) + ", " + str(var) + ") " + " and cmax less than or equal to/greater than " + str(cmax_median) + " the average pmf variance is \n(" + str(mean(var_o_averaged_list_less)) +  ", " + str(mean(var_o_averaged_list_more)) + ")")
                        
    else:
        if graph_mu:
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
                        #now, for each cmax value, get the mean of the pmf variances
                        cmax_list = []
                        mu_o_averaged_list = []
                        #go through each cmax
                        for cmax in cmax_vals:
                            #append the cmax to a list to keep track of which cmax goes with the averaged var_o
                            cmax_list.append(cmax)
                            #get the df for only this failure value, mean, variance, and cmax
                            separated_by_f_mu_var_and_cmax_df = separated_by_f_mu_and_var_df[separated_by_f_mu_and_var_df['Cmax'] == cmax]
                            #append the averaged mean_o to the mean_o_averaged_list
                            mu_o_averaged_list.append(mean(separated_by_f_mu_var_and_cmax_df['mu_o']))
                        #print the pearsonr (correlation) between the two lists
                        correlation, p_value = pearsonr(cmax_list, mu_o_averaged_list)
                        print("The correlation is ", str(correlation), " with a p-value of ", str(p_value))
                        #create a dictionary for the plot off of these two lists
                        plot_dict = {'Cmax' : cmax_list, 'mu_o' : mu_o_averaged_list}
                        plot_df = pd.DataFrame(plot_dict)
                        #graph the cmax versus the pmf variance averaged
                        fig = plt.figure()
                        plt.plot('Cmax', 'mu_o', data=plot_df, color='skyblue', marker='o', linewidth=1)
                        plt.xlabel('Cmax')
                        plt.ylabel('Mean of PMF (Output)')
                        title = 'cmax versus pmf mean for f = ' + str(f) + ", mean = " +  str(mu) + ", and variance = " + str(var)
                        plt.title(title)
                        # show legend
                        plt.legend()
                        plt.show()
        else:
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
                        #now, for each cmax value, get the mean of the pmf variances
                        cmax_list = []
                        var_o_averaged_list = []
                        #go through each cmax
                        for cmax in cmax_vals:
                            #append the cmax to a list to keep track of which cmax goes with the averaged var_o
                            cmax_list.append(cmax)
                            #get the df for only this failure value, mean, variance, and cmax
                            separated_by_f_mu_var_and_cmax_df = separated_by_f_mu_and_var_df[separated_by_f_mu_and_var_df['Cmax'] == cmax]
                            #append the averaged var_o to the var_o_averaged_list
                            var_o_averaged_list.append(mean(separated_by_f_mu_var_and_cmax_df['var_o']))
                        #print the pearsonr (correlation) between the two lists
                        correlation, p_value = pearsonr(cmax_list, var_o_averaged_list)
                        print("The correlation is ", str(correlation), " with a p-value of ", str(p_value))
                        #create a dictionary for the plot off of these two lists
                        plot_dict = {'Cmax' : cmax_list, 'var_o' : var_o_averaged_list}
                        plot_df = pd.DataFrame(plot_dict)
                        #graph the cmax versus the pmf variance averaged
                        fig = plt.figure()
                        plt.plot('Cmax', 'var_o', data=plot_df, color='skyblue', marker='o', linewidth=1)
                        plt.xlabel('Cmax')
                        plt.ylabel('Variance of PMF (Output)')
                        title = 'cmax versus pmf variance for f = ' + str(f) + ", mean = " +  str(mu) + ", and variance = " + str(var)
                        plt.title(title)
                        # show legend
                        plt.legend()
                        plt.show()
                    