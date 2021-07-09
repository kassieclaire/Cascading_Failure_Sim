#TODO: convert run.m to python
from findStateSpace import FindStateSpace
topology = 'case118'
iterations = 100
initialFailures = 3
loadGenerationRatio = .7
loadShedConstant = .97
capacityEstimationError = .02
States=find_state_space(topology, iterations, initialFailures, loadGenerationRatio, loadShedConstant, capacityEstimationError);
