%%IEEE118
% clear;
% topology = 'case118';
% iterations = 10000;
% initialFailures = 3;
% loadGenerationRatio = .7;
% loadShedConstant = .97;
% capacityEstimationError = .02;
% [States, Initial_Failure_Table]=S_FindingStateSpace_ANN_dataset_function(topology, iterations, initialFailures, loadGenerationRatio, loadShedConstant, capacityEstimationError);
% save('states_IEEE118.mat', 'States')
% save('initial_failures_IEEE118.mat', 'Initial_Failure_Table')
%%IEEE39_2
clear;
topology = 'case39';
iterations = 10;
initialFailures = 2;
loadGenerationRatio = .9; %reduce R
loadShedConstant = .97;
capacityEstimationError = .02;

[States, Initial_Failure_Table]=S_FindingStateSpace_ANN_dataset_function(topology, iterations, initialFailures, loadGenerationRatio, loadShedConstant, capacityEstimationError);
save('states_IEEE39_2.mat', 'States')
save('initial_failures_IEEE39_2.mat', 'Initial_Failure_Table')
%%TABLE CREATION CODE
%extra code to create table out of Matrix
col_names = {'Total Line Failures', 'Maximum failed line capacity', 'Load shed from previous step', 'Difference in Load Shed','Load', 'Free Space 1', 'Free Space 2', 'Steady State','Capacity of Failed Ones', 'Capacity of Failed Ones 2', 'Failed Line Index', 'Capacity of Failed One', 'Time of Failure Event', 'Accumulation of Failed Capacities', 'Free Space 3', 'Demand-Loadshed Difference', 'Free Space 4', 'Generation'};
states_table = array2table(States,'VariableNames',col_names);
writetable(states_table,'IEEE39_States_Table.csv')
%%IEEE300
% clear;
% topology = 'case300';
% iterations = 10000;
% initialFailures = 3;
% loadGenerationRatio = .7;
% loadShedConstant = .97;
% capacityEstimationError = .02;

% [States, Initial_Failure_Table]=S_FindingStateSpace_ANN_dataset_function(topology, iterations, initialFailures, loadGenerationRatio, loadShedConstant, capacityEstimationError);
% save('states_IEEE300.mat', 'States')
% save('initial_failures_IEEE300.mat', 'Initial_Failure_Table')
%%Polish_Grid
% clear;
% topology = 'case2383wp';
% iterations = 100;
% initialFailures = 6;
% loadGenerationRatio = .7;
% loadShedConstant = .97;
% capacityEstimationError = .02;
% 
% [States, Initial_Failure_Table]=S_FindingStateSpace_ANN_dataset_function(topology, iterations, initialFailures, loadGenerationRatio, loadShedConstant, capacityEstimationError);
% save('states_Polish.mat', 'States')
% save('initial_failures_Polish.mat', 'Initial_Failure_Table')
%ACTIVSg200
% clear;
% topology = 'ACTIVSg2000';
% iterations = 10;
% initialFailures = 3;
% loadGenerationRatio = .7;
% loadShedConstant = .97;
% capacityEstimationError = .02;
% [States, Initial_Failure_Table]=S_FindingStateSpace_ANN_dataset_function(topology, iterations, initialFailures, loadGenerationRatio, loadShedConstant, capacityEstimationError);
% save('states_ACTIVSg2000.mat', 'States')
% save('initial_failures_IACTIVSg2000.mat', 'Initial_Failure_Table')