import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit as cf

#NOTE: look at number of pairs within distance of each other to measure clustering behavior
#graph the distance distribution of each pair of points
#how close are the points together?
#set the plot style to ieee
#look at the shape of the function
#the interaction function
#s as a function of r
plt.style.use('ieee')
#update the plot dpi
plt.rcParams['figure.dpi'] = 350
#set the figure size
plt.rcParams['figure.figsize'] = (4, 3)
#set plot font size to 10
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
    #round input mean values to closest 0.5
    input_mean_vals = np.around(input_mean_vals, decimals=1)
    #get unique input mean values
    input_mean_vals = input_mean_vals.unique()
    #iterate through the input means, get the output variances and means, and curve fit the output variances and output means vs the input variances
    for mu_i in input_mean_vals:
        #get the output and input variances for this input mean
        output_var_vals = df[(df['F'] == f) & (np.around(df['mu_i'], decimals = 1) == mu_i)]['var_o']
        input_var_vals = df[(df['F'] == f) & (np.around(df['mu_i'], decimals = 1) == mu_i)]['var_i']
        #get the output means for this input mean
        output_mean_vals = df[(df['F'] == f) & (np.around(df['mu_i'], 1) == mu_i)]['mu_o']
        #get the unique input variances
        unique_input_var_vals = input_var_vals.unique()
        #create an empty list to store mean output variances
        mean_output_var_vals = []
        #create an empty list to store mean output means
        mean_output_mean_vals = []
        #iterate through the unique input variances
        for var_i in unique_input_var_vals:
            #get the mean of the output variances for this input variance and append to the mean output variances list
            mean_output_var_vals.append(np.mean(output_var_vals[input_var_vals == var_i]))
            #get the mean of the output means for this input variance and append to the mean output means list
            mean_output_mean_vals.append(np.mean(output_mean_vals[input_var_vals == var_i]))
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
            #graph the mean output variance vs unique input variances as points in green
            plt.plot(unique_input_var_vals, mean_output_var_vals, 'o', color='green', label='mean')
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
            #graph the mean output mean vs unique input variances as points in purple
            plt.plot(unique_input_var_vals, mean_output_mean_vals, 'o', color='purple', label='mean')
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
    #round input variance values to closest 0.1
    input_var_vals = np.around(input_var_vals, decimals=1)
    #get unique input variance values
    input_var_vals = input_var_vals.unique()
    #iterate through the input variances, get the output variances and means, and curve fit the output variances and output means vs the input means
    for var_i in input_var_vals:
        #round the input variance to the closest 0.5
        var_i = round(var_i, 1)
        #get the output and input variances for this input variance
        output_var_vals = df[(df['F'] == f) & (np.around(df['var_i'],1) == var_i)]['var_o']
        input_mean_vals = df[(df['F'] == f) & (np.around(df['var_i'],1) == var_i)]['mu_i']
        #get the output means for this input variance
        output_mean_vals = df[(df['F'] == f) & (np.around(df['var_i'], 1) == var_i)]['mu_o']
        #get the unique input mean vals
        unique_input_mean_vals = input_mean_vals.unique()
        #create an empty list to store mean output variances
        mean_output_var_vals = []
        #create an empty list to store mean output means
        mean_output_mean_vals = []
        #iterate through the unique input means
        for mu_i in unique_input_mean_vals:
            #get the mean of the output variances for this input mean and append to the mean output variances list
            mean_output_var_vals.append(np.mean(output_var_vals[input_mean_vals == mu_i]))
            #get the mean of the output means for this input mean and append to the mean output means list
            mean_output_mean_vals.append(np.mean(output_mean_vals[input_mean_vals == mu_i]))
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
            #graph the mean output variance vs unique input means as points in green
            plt.plot(unique_input_mean_vals, mean_output_var_vals, 'o', color='green', label='mean')
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
            #graph the mean output mean vs unique input means as points in purple
            plt.plot(unique_input_mean_vals, mean_output_mean_vals, 'o', color='purple', label='mean')
            #add gridlines to the plot
            plt.grid(True)
            #label the graph
            plt.xlabel('Input Mean')
            plt.ylabel('Output Mean')
            plt.title('Output Mean vs Input Mean for F = ' + str(f) + ' and var_i = ' + str(round(var_i, 3)))
            plt.legend()
            plt.show()
        

    
    



