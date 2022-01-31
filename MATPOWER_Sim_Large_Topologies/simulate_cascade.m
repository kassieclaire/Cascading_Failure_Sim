function simulate_cascade(CaseName, Iterations, InitialFailures, LoadGenerationRatio, LoadShedConstant, EstimationError, output_name, batch_size)
default_group_size = 32;
if nargin > 7
    group_size = str2num(batch_size);
    Iterations = str2num(Iterations);
    InitialFailures=str2num(InitialFailures);
    LoadGenerationRatio=str2double(LoadGenerationRatio);
    LoadShedConstant=str2double(LoadShedConstant);
    EstimationError=str2double(EstimationError);
    if_name = append(output_name, '_if', '.mat'); %'if' stands for "initial failures"
    sm_name = append(output_name, '_sm', '.mat'); %'sm' stands for "states matrix"
elseif nargin > 0
    group_size = default_group_size;
    Iterations = str2num(Iterations);
    InitialFailures=str2num(InitialFailures);
    LoadGenerationRatio=str2double(LoadGenerationRatio);
    LoadShedConstant=str2double(LoadShedConstant);
    EstimationError=str2double(EstimationError);
    if_name = append(output_name, '_if', '.mat'); %'if' stands for "initial failures"
    sm_name = append(output_name, '_sm', '.mat'); %'sm' stands for "states matrix"
else %number of arguments 0, read from file instead
    %fileID = fopen('inputs.txt', 'r');
    %formatSpec = '%s';
    %inputs = fscanf(fileID, formatSpec)
    inputs = convertStringsToChars(readlines("input.txt"))
    if length(inputs) > 7
        group_size = inputs(8);
        group_size = str2num(group_size{1});
    else
        group_size = default_group_size;
    end
    CaseName = inputs(1);
    CaseName = CaseName{1}
    Iterations = inputs(2);
    Iterations = str2num(Iterations{1});
    InitialFailures = inputs(3);
    InitialFailures = str2num(InitialFailures{1});
    LoadGenerationRatio=inputs(4);
    LoadGenerationRatio=str2double(LoadGenerationRatio{1});
    LoadShedConstant=inputs(5);
    LoadShedConstant=str2double(LoadShedConstant{1});
    EstimationError = inputs(6);
    EstimationError=str2double(EstimationError{1});
    output_name = inputs(7);
    if_name = append(output_name{1}, '_if', '.mat'); %'if' stands for "initial failures"
    sm_name = append(output_name{1}, '_sm', '.mat'); %'sm' stands for "states matrix"
end
[States, Initial_Failure_Table] = S_FindingStateSpace_ANN_dataset_function(CaseName, Iterations, InitialFailures, LoadGenerationRatio, LoadShedConstant, EstimationError, group_size);
save(sm_name, 'States');
save(if_name, 'Initial_Failure_Table');
end