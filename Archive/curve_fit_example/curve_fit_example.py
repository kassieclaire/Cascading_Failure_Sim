# fit a second degree polynomial to the economic data
from numpy import arange
from pandas import read_csv
from scipy.optimize import curve_fit
from matplotlib import pyplot

# define the true objective function
def objective(input, a, b, c):
	return a * input[:, 0] + b * input[:, 0]**2 + c

# load the dataset
url = 'https://raw.githubusercontent.com/jbrownlee/Datasets/master/longley.csv'
dataframe = read_csv(url, header=None)
print(dataframe)
data = dataframe.values
# choose the input and output variables
input, output = [data[:, 3], data[:, 4]], data[:, -1]
# curve fit
popt, _ = curve_fit(objective, input, output)
# summarize the parameter values
a, b, c = popt
print('y = %.5f * x + %.5f * x^2 + %.5f' % (a, b, c))
# plot input vs output
#pyplot.scatter(input, )
# define a sequence of inputs between the smallest and largest known inputs
#x_line = arange(min(x), max(x), 1)
# calculate the output for the range
#y_line = objective(x_line, a, b, c)
# create a line plot for the mapping function
#pyplot.plot(x_line, y_line, '--', color='red')
pyplot.show()