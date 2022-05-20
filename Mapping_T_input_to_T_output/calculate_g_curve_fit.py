import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit as cf

#set the plot style to ieee
plt.style.use('ieee')
#update the plot dpi
plt.rcParams['figure.dpi'] = 350
#set the figure size
plt.rcParams['figure.figsize'] = (4, 3)
#set plot font size to 6
plt.rcParams.update({'font.size': 6})

#set a minimum number of failures
min_f = 7
#import the mean and variance csv as a dataframe
df = pd.read_csv('mean_and_variance.csv')
#find unique F values and iterate through these
failure_vals = df["F"].unique()
#cut off the failure values that are less than the minimum number of failures
failure_vals = failure_vals[failure_vals >= min_f]
#iterate through the failure values
for f in failure_vals:
    #get the input variances and means for this failure value
    input_mean_vals = df[df['F'] == f]['mu_i']
    #iterate through the input means, get the output variances and means, and curve fit the output variances and output means vs the input variances
    for mu_i in input_mean_vals:
        #get the output and input variances for this input mean
        output_var_vals = df[(df['F'] == f) & (df['mu_i'] == mu_i)]['var_o']
        input_var_vals = df[(df['F'] == f) & (df['mu_i'] == mu_i)]['var_i']
        #get the output means for this input mean
        output_mean_vals = df[(df['F'] == f) & (df['mu_i'] == mu_i)]['mu_o']
        #check that there is more than one output variance value
        if len(output_var_vals) > 1:
            #curve fit the output variance vs input variance
            fit_params = cf(lambda x, a, b: a*x + b, input_var_vals, output_var_vals)
            #get the slope and intercept of the fit
            slope = fit_params[0][0]
            intercept = fit_params[0][1]
            #graph the output variance vs input variance with the fit
            plt.plot(input_var_vals, output_var_vals, 'o', label='data')
            plt.plot(input_var_vals, slope*input_var_vals + intercept, '-', label='fit')
            #add gridlines to the plot
            plt.grid(True)
            #label the graph
            plt.xlabel('Input Variance')
            plt.ylabel('Output Variance')
            plt.title('Output Variance vs Input Variance for F = ' + str(f) + ' and mu_i = ' + str(round(mu_i, 3)))
            plt.legend()
            plt.show()
        #check that there is more than one output mean value
        if len(output_mean_vals) > 1:
            #curve fit the output mean vs input variance
            fit_params = cf(lambda x, a, b: a*x + b, input_var_vals, output_mean_vals)
            #get the slope and intercept of the fit
            slope = fit_params[0][0]
            intercept = fit_params[0][1]
            #graph the output mean vs input variance with the fit
            plt.plot(input_var_vals, output_mean_vals, 'o', label='data')
            plt.plot(input_var_vals, slope*input_var_vals + intercept, '-', label='fit')
            #add gridlines to the plot
            plt.grid(True)
            #label the graph
            plt.xlabel('Input Variance')
            plt.ylabel('Output Mean')
            plt.title('Output Mean vs Input Variance for F = ' + str(f) + ' and mu_i = ' + str(round(mu_i, 3)))
            plt.legend()
            plt.show()
    #find input variances for this failure value
    input_var_vals = df[df['F'] == f]['var_i']
    #iterate through the input variances, get the output variances and means, and curve fit the output variances and output means vs the input means
    for var_i in input_var_vals:
        #get the output and input variances for this input variance
        output_var_vals = df[(df['F'] == f) & (df['var_i'] == var_i)]['var_o']
        input_mean_vals = df[(df['F'] == f) & (df['var_i'] == var_i)]['mu_i']
        #get the output means for this input variance
        output_mean_vals = df[(df['F'] == f) & (df['var_i'] == var_i)]['mu_o']
        #check that there is more than one output variance value
        if len(output_var_vals) > 1:
            #curve fit the output variance vs input mean
            fit_params = cf(lambda x, a, b: a*x + b, input_mean_vals, output_var_vals)
            #get the slope and intercept of the fit
            slope = fit_params[0][0]
            intercept = fit_params[0][1]
            #graph the output variance vs input mean with the fit
            plt.plot(input_mean_vals, output_var_vals, 'o', label='data')
            plt.plot(input_mean_vals, slope*input_mean_vals + intercept, '-', label='fit')
            #add gridlines to the plot
            plt.grid(True)
            #label the graph
            plt.xlabel('Input Mean')
            plt.ylabel('Output Variance')
            plt.title('Output Variance vs Input Mean for F = ' + str(f) + ' and var_i = ' + str(round(var_i, 3)))
            plt.legend()
            plt.show()
        #check that there is more than one output mean value
        if len(output_mean_vals) > 1:
            #curve fit the output mean vs input mean
            fit_params = cf(lambda x, a, b: a*x + b, input_mean_vals, output_mean_vals)
            #get the slope and intercept of the fit
            slope = fit_params[0][0]
            intercept = fit_params[0][1]
            #graph the output mean vs input mean with the fit
            plt.plot(input_mean_vals, output_mean_vals, 'o', label='data')
            plt.plot(input_mean_vals, slope*input_mean_vals + intercept, '-', label='fit')
            #add gridlines to the plot
            plt.grid(True)
            #label the graph
            plt.xlabel('Input Mean')
            plt.ylabel('Output Mean')
            plt.title('Output Mean vs Input Mean for F = ' + str(f) + ' and var_i = ' + str(round(var_i, 3)))
            plt.legend()
            plt.show()
        

    
    



