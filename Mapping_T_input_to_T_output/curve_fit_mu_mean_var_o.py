from numpy import corrcoef, sort
import pandas as pd
import matplotlib.pyplot as plt
from statistics import mean, median
from scipy.stats import pearsonr
#include curve_fit
from scipy.optimize import curve_fit

df = pd.read_csv('mean_and_variance.csv')
#find unique F values and iterate through these
failure_vals = df["F"].unique()
for f in failure_vals:
    #get the df for only this failure value
    separated_by_f_df = df[df['F'] == f]
    #find unique input means for that F and iterate through these
    input_mean_vals = separated_by_f_df['mu_i'].unique()
    for mu_i in input_mean_vals:
        #get the df for only this failure value and mean
        separated_by_f_and_mu_df = separated_by_f_df[separated_by_f_df['mu_i'] == mu_i]
        #find input variances for that F and input mean and iterate through these
        input_var_vals = separated_by_f_and_mu_df['var_i']
        # get the output variance values for this number of failures, input mean
        output_var_vals = separated_by_f_and_mu_df['var_o']
        #check that the number of input variances is the same as the number of output variances
        if len(input_var_vals) != len(output_var_vals):
            print("Error: number of input variances is not the same as the number of output variances")
            #skip to the next input mean
            continue
        #check that there is more than one output variance value
        if len(output_var_vals) < 2:
            print("Error: there is only one output variance value")
            #skip to the next input mean
            continue
        #check that there is more than one input variance value
        if len(input_var_vals) < 2:
            print("Error: there is only one input variance value")
            #skip to the next input mean
            continue
        #curve fit the output variance vs input variance
        fit_params = curve_fit(lambda x, a, b: a*x + b, input_var_vals, output_var_vals)
        #get the slope and intercept of the fit
        slope = fit_params[0][0]
        intercept = fit_params[0][1]
        #graph the output variance vs input variance with the fit
        plt.plot(input_var_vals, output_var_vals, 'o', label='data')
        plt.plot(input_var_vals, slope*input_var_vals + intercept, '-', label='fit')
        #label the graph
        plt.xlabel('Input Variance')
        plt.ylabel('Output Variance')
        plt.title('Output Variance vs Input Variance for F = ' + str(f) + ' and mu_i = ' + str(mu_i))
        plt.legend()
        plt.show()