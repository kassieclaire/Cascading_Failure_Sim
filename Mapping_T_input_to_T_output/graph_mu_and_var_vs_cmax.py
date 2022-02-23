from numpy import sort
import pandas as pd
import matplotlib.pyplot as plt
from statistics import mean
from scipy.stats import pearsonr
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
                