import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit as cf
#make a list of integers from 1 to 10
x = np.arange(1, 11)
#make a list of 10 random y values
y = np.random.rand(10)
#curve fit y vs x
fit_params = cf(lambda x, a, b: a*x + b, x, y)
#create a new figure
fig = plt.figure()
#graph the y vs x with the fit
plt.plot(x, y, 'o', label='data')
plt.plot(x, fit_params[0][0]*x + fit_params[0][1], '-', label='fit')
#add gridlines to the plot
plt.grid(True)
#label the graph
plt.xlabel('x')
plt.ylabel('y')
plt.title('y vs x')
plt.legend()
plt.show()
