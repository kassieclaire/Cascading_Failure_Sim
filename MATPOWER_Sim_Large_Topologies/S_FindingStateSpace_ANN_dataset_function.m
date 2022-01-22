function [States, IniFtable] = S_FindingStateSpace_ANN_dataset_function(CaseName, Iterations, InitialFailures, LoadGenerationRatio, LoadShedConstant, EstimationError, batch_size) %Add initial_failure_cluster variable, set by default to -1
%Function that returns a state space for (Topology, # of iterations, # of initial failures, load-generation ratio (r), LoadShedConstant (\theta), and capcacity estimation error (e))
%clc;
%clear all;
%close all;
define_constants;
%CaseName='case300';
%define the batch size
simulation_group_size = batch_size;

%[originalNumBus, originalNumGen, originalNumBran, NumBuses, mpc1, LoadGenMatch, Generation, Demand, DemandIndex, FakeCapRate, FlowCap TrueCaps, NumBranches, WhichInitialLoad, OriginalMPC] = prepareCase(CaseName);

FakeCapRate = 1; % fake capacity
%% Parameter initialization
TrueCaps=[50 100 200 400 800]; % quantized capacity
%% Initial load on which the capacity of lines will be determined
mpc1 = loadcase(CaseName);
mpc1 = S_ReadyTheCase(mpc1);
%% keep the original values of number of buses and gens and branches before changing
originalNumBus=length(mpc1.bus(:,1));
originalNumGen=length(mpc1.gen(:,1));
originalNumBran=length(mpc1.branch(:,1));
NumBuses = length(mpc1.bus(:,1));
NumBranches = originalNumBran;
%% Seperate the buses with both load and generators into seperate load and generator buses
[mpc1 LoadGenMatch] = S_SeperateGenAndLoad(mpc1);

[WhichInitialLoad, Generation, Demand, DemandIndex] = S_FindFullLoadOfGrid(mpc1);

%% Calculating the total demand and generation capacity of the grid%%%%%
%if strcmp(CaseName, 'case2383wp')
%   [WhichInitialLoad, Generation, Demand, DemandIndex] = S_FindFullLoadOfGrid_LargeGrid(mpc1);
%else
%   [WhichInitialLoad, Generation, Demand, DemandIndex] = S_FindFullLoadOfGrid(mpc1);
%end
%%
clear mpc1; % clear because
mpc1 = loadcase(CaseName);
%reduce information in branch, bus, gen, gencost if more than needed
mpc1 = reduce_information(mpc1);
%Ready the case
mpc1 = S_ReadyTheCase(mpc1);
%% check if any negative load
for i=1:NumBuses
    if (mpc1.bus(i,3)<0) % if the real power of the bus is negative
        mpc1.bus(i,3) = abs(mpc1.bus(i,3));
    end
end
%% Seperate the buses with both load and generators into seperate load and generator buses
[mpc1 LoadGenMatch] = S_SeperateGenAndLoad(mpc1);
%% Find installed capacity of a transmission line and use it as rateA threshold
[Capacity, FlowCap] = S_CapFinder(WhichInitialLoad,mpc1,TrueCaps,originalNumBran);
mpc1.branch(:,6) = FakeCapRate*Capacity;
CountCaps=zeros(1,length(TrueCaps));
for i=1:length(TrueCaps)
    CountCaps(i)=sum(Capacity==TrueCaps(i));
end
%% Reset mpc1, PD: take mpc with separated load and generator
OriginalMPC = mpc1; % this is the MPC with separated load and generator
clear mpc1;
%% initialize parameters
DGRatioVector = [LoadGenerationRatio];% r
%DGRatioVector = [0.5, .55, 0.6, .65, 0.7, .75, 0.8, .85, 0.9,];
len_DGRatioVector = length(DGRatioVector);
%DeltaVector = [0.01 .025, 0.05, .075, 0.1, .125, 0.15, .175,  0.2, .225,  0.25, .275, 0.3, .35, .4, .45, .5];
DeltaVector = [EstimationError];
len_DeltaVector = length(DeltaVector);% e
%NoCoopPercentageVector = [0.01 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4,0.45 0.5,0.55,.6,.65,.7,.75,.8,.85,.9]; % theta
NoCoopPercentageVector = [LoadShedConstant]; % theta
%NoCoopPercentageVector = [0.01 0.05, 0.1, 0.15, 0.2, 0.25, 0.3,]; % theta
%NoCoopPercentageVector = [0.01 .025, 0.05, .075, 0.1, .125, 0.15, .175,  0.2, .225,  0.25, .275, 0.3,35,.4]; % theta
len_NoCoopPercentageVector = length(NoCoopPercentageVector);
%FixedFailProbvector = [0, 0.01, 0.02, 0.03, 0.04, 0.05]; % fixed probability of failure for neighbors
%len_FixedFailProbvector = length(FixedFailProbvector);
betavector = [0];
beta = betavector(randi(length(betavector)));
%%

NumIt = Iterations;
%% Generate an initial failure table
iniFailNodes = [];
for i=1:NumIt
    b=InitialFailures;
    %2 or 3 failures
    % b=1+ceil(9*rand);
    %if initial_failure_cluster != -1
        %then use initial failures only from cluster
    %end
    %else
    %do this
    randomindex=randperm(NumBranches); %change this line in order to add cluster-specific initial failures
    %TODO: change so that it takes a random permutation of the vector of
    %branches in the cluster
    %end
    temp=randomindex(1:b);
    %  iniFailNodes = [iniFailNodes;temp];
    IniFidx=randomindex(1:b);
    
    IniFtable{1,i} = IniFidx;
    clear IniFidx
end
%%
mpc1 = OriginalMPC; % this is the MPC with separated load and generator
BranchMatrix=mpc1.branch;
NumBranches=length(BranchMatrix(:,1));
BusMatrix=mpc1.bus;
NumBuses=length(BusMatrix(:,1));
GenMatrix=mpc1.gen;
NumGens=length(GenMatrix(:,1));
StateCounter = 0; %counts the number of possible states
clear States;
%limit = 10000;
%States = zeros(limit,18);
tic
% for s=1:NumIt
%     if StateCounter > limit * 0.99
%         break;
%     end
%     s
%     States = S_DCPowerFlowSimulation_ANN_dataset(OriginalMPC, NumBranches, NoCoopPercentageVector, StateCounter, TrueCaps, DGRatioVector, WhichInitialLoad, Capacity, s, IniFtable, len_DGRatioVector, len_DeltaVector, DeltaVector, len_NoCoopPercentageVector, FlowCap, DemandIndex);
%
%     %clear mpc1
%     toc
% end

%Save the initial failure table in a temporary file in case simulation
%fails, this way data is salvageable
save("temp_if_salvage", "IniFtable");

%Parallelization added by Kassie Povinelli
%Grouping added by Kassie povinelli (2021-12-24)
%Grouping preserves system RAM by storing results from previous simulations
%in .mat files. This is to fix issues when working with larger simulations.
%A recommended group size depends on the system RAM size, but for a system
%with 16GB RAM, keep group sizes in the 100s and below 1000 (errors occur
%around 5000 with IEEE300)
%keep track of how many errors
failure_track = 0;


if (NumIt > simulation_group_size)
    num_simulation_groups = ceil(NumIt / simulation_group_size);
    fprintf("Number of iterations exceeds amount allowed for single group. Splitting into %d simulations of max size %d\n\r", num_simulation_groups, simulation_group_size);
    for k=1:num_simulation_groups
        start_index = (k-1)*simulation_group_size + 1; %start index
        %end_index;
        %calculate end index
        if (k == num_simulation_groups && mod(NumIt, simulation_group_size) ~= 0)
            end_index = start_index + mod(NumIt, simulation_group_size) - 1;
        else
            end_index = start_index + simulation_group_size - 1;
        end
        %start the group of simulations in parallel
        fprintf("Starting simulations from starting index %d to ending index %d\n\r", start_index, end_index);
        StatesCell = cellmat((end_index-start_index+1), 1, 10000, 14);
        final_index = (end_index-start_index+1);
        parfor s=1:final_index % for every iteration under the same setting
            %s %print out s
            success = 0;
            state_number = start_index + s - 1;
            %DC code
            %StatesCell(s, 1) = {DCPowerFlowSimulation(OriginalMPC, NumBranches, NoCoopPercentageVector, StateCounter, TrueCaps, DGRatioVector, WhichInitialLoad, Capacity, s, IniFtable, len_DGRatioVector, len_DeltaVector, DeltaVector, len_NoCoopPercentageVector, FlowCap, DemandIndex)};
            %AC code
            while (success == 0)
                StatesCell(s, 1) = {S_DCPowerFlowSimulation_ANN_dataset(OriginalMPC, NumBranches, NoCoopPercentageVector, StateCounter, TrueCaps, DGRatioVector, WhichInitialLoad, Capacity, state_number, IniFtable, len_DGRatioVector, len_DeltaVector, DeltaVector, len_NoCoopPercentageVector, FlowCap, DemandIndex)};
                States_Matrix = StatesCell{s, 1};
                if States_Matrix(1,1) ~= -2
                    success = 1;
                else
                    %otherwise try again
                    fprintf("Restarting simulation...\n");
                end
            end
        end
        %Temporary -- turn states cell array back to array
        States = cell2mat(StatesCell); %Turn cells to states matrix
        simulation_group_name = strcat("temp_", num2str(k));
        save(simulation_group_name, "States");
        clear StatesCell;
        clear States;
    end
    %recombine the simulation data
    group_states = load("temp_1.mat").States;
    %could be done better, but not sure how currently
    States = group_states;
    for k=2:num_simulation_groups
        group_name = strcat("temp_", num2str(k), ".mat");
        group_states = load(group_name).States;
        States = vertcat(States, group_states);
        %States = [States;group_states];
    end
    %check if things make sense
    if (length(find(States(:,8)==-1)) ~= NumIt)
        fprintf("ERROR: Simulation results do not match number of iterations. Simulation results indicate %d runs, number of iterations should have been %d.\n\r", length(find(States(:,8)==-1)) , NumIt);
    end
    %clean up temporary files
    for k=1:num_simulation_groups
        group_name = strcat("temp_", num2str(k), ".mat");
        delete(group_name);
    end

else
    StatesCell = cellmat(NumIt, 1, 1000, 14);
    parfor s=1:NumIt % for every iteration under the same setting
        %s %print out s
        success = 0;
        %DC code
        %StatesCell(s, 1) = {DCPowerFlowSimulation(OriginalMPC, NumBranches, NoCoopPercentageVector, StateCounter, TrueCaps, DGRatioVector, WhichInitialLoad, Capacity, s, IniFtable, len_DGRatioVector, len_DeltaVector, DeltaVector, len_NoCoopPercentageVector, FlowCap, DemandIndex)};
        %AC code
        while (success == 0)
            StatesCell(s, 1) = {S_DCPowerFlowSimulation_ANN_dataset(OriginalMPC, NumBranches, NoCoopPercentageVector, StateCounter, TrueCaps, DGRatioVector, WhichInitialLoad, Capacity, s, IniFtable, len_DGRatioVector, len_DeltaVector, DeltaVector, len_NoCoopPercentageVector, FlowCap, DemandIndex)};
            States_Matrix = StatesCell{s, 1};
            if States_Matrix(1,1) ~= -2
                success = 1;
            else
                %otherwise try again
                fprintf("Restarting simulation...\n");
            end
        end
    end
    %Temporary -- turn states cell array back to array
    States = cell2mat(StatesCell); %Turn cells to states matrix
end
if failure_track > 0
    fprintf("%d iterations of simulation required restart. \n", failure_track);
end
   %

toc
end