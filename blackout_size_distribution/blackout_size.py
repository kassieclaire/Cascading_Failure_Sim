#transform this matlab code into python code:
#Blackoutsize=zeros(NumBranches,1);
# for i=1:length(States(:,1))
#     if(States(i,8)==-1)
#         Blackoutsize(States(i,1))=Blackoutsize(States(i,1))+1;
#     end
# end
# bar(Blackoutsize/sum(Blackoutsize));

#python code:
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#set the number of branches (186 for IEEE 118, 46 for IEEE 39, look up for others)
num_branches = 186
#load the states dataframe csv file from the folder states_dfs
states_df = pd.read_csv('states_dfs/states_dataframe.csv')
#make an array of zeros Blackoutsize with the same length as the number of branches
blackoutsize = np.zeros(num_branches)
#loop through the entire states dataframe, row by row
for index, row in states_df.iterrows():
    #check if the state is a stable state
    if row['Steady State'] == -1:
        #if the state is a stable state, add 1 to the Blackoutsize array
        blackoutsize[row['Total Line Failures']] += 1
#plot the Blackoutsize array as a bar graph
plt.bar(np.arange(num_branches), blackoutsize/sum(blackoutsize))
#set the title of the graph
plt.title('Blackout Size Distribution')
#set the x-axis label
plt.xlabel('Number of Line Failures')
#set the y-axis label
plt.ylabel('Probability')
#show the graph
plt.show()
