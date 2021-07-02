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
%%IEEE39
% clear;
% topology = 'case39';
% iterations = 10000;
% initialFailures = 4;
% loadGenerationRatio = .7;
% loadShedConstant = .97;
% capacityEstimationError = .02;
% 
% [States, Initial_Failure_Table]=S_FindingStateSpace_ANN_dataset_function(topology, iterations, initialFailures, loadGenerationRatio, loadShedConstant, capacityEstimationError);
% save('states_IEEE39.mat', 'States')
% save('initial_failures_IEEE39.mat', 'Initial_Failure_Table')
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
clear;
topology = 'case2383wp';
iterations = 100;
initialFailures = 6;
loadGenerationRatio = .7;
loadShedConstant = .97;
capacityEstimationError = .02;

[States, Initial_Failure_Table]=S_FindingStateSpace_ANN_dataset_function(topology, iterations, initialFailures, loadGenerationRatio, loadShedConstant, capacityEstimationError);
save('states_Polish.mat', 'States')
save('initial_failures_Polish.mat', 'Initial_Failure_Table')
