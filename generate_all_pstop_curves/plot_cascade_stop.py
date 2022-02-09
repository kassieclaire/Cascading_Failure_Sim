import matplotlib.pyplot as plt
def plot_p_stop(p_stop_df, variable_name):  
    fig = plt.figure()
    plt.plot('x_values', 'cascade_stop', data=p_stop_df, color='skyblue', linewidth=1)
    plt.xlabel(variable_name)
    plt.ylabel('Cascade-Stop Probability')
    plt.title('Cascade-Stop Probability vs ' + variable_name)
    # show legend
    plt.legend()
    #set title
    plt.title = "Cascade-Stop Probability vs " + variable_name
    plt.show()