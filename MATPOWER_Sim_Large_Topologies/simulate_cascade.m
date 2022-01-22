function simulate_cascade(CaseName, Iterations, InitialFailures, LoadGenerationRatio, LoadShedConstant, EstimationError, output_name, batch_size)
if nargin > 7
    group_size = str2num(batch_size);
else
    group_size = 32;
end
Iterations = str2num(Iterations);
InitialFailures=str2num(InitialFailures);
LoadGenerationRatio=str2double(LoadGenerationRatio);
LoadShedConstant=str2double(LoadShedConstant);
EstimationError=str2double(EstimationError);
if_name = append(output_name, '_if', '.mat'); %'if' stands for "initial failures"
sm_name = append(output_name, '_sm', '.mat'); %'sm' stands for "states matrix"
[States, Initial_Failure_Table] = S_FindingStateSpace_ANN_dataset_function(CaseName, Iterations, InitialFailures, LoadGenerationRatio, LoadShedConstant, EstimationError, group_size);
save(sm_name, 'States');
save(if_name, 'Initial_Failure_Table');
end