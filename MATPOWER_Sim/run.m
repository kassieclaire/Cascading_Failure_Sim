topology = 'case118';
iterations = 100;
initialFailures = 3;
loadGenerationRatio = .7;
loadShedConstant = .97;
capacityEstimationError = .02;

States=S_FindingStateSpace_ANN_dataset_function(topology, iterations, initialFailures, loadGenerationRatio, loadShedConstant, capacityEstimationError);