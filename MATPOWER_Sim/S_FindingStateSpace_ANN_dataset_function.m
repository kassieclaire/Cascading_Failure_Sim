function [States, IniFtable] = S_FindingStateSpace_ANN_dataset_function(CaseName, Iterations, InitialFailures, LoadGenerationRatio, LoadShedConstant, EstimationError)
%Function that returns a state space for (Topology, # of iterations, # of initial failures, load-generation ratio (r), LoadShedConstant (\theta), and capcacity estimation error (e))
%clc;
%clear all;
%close all;
define_constants;
%CaseName='case300';

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
    %2 or 3 failures
    % b=1+ceil(9*rand);
    b=InitialFailures;
    randomindex=randperm(NumBranches);
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
limit = 10000;
States = zeros(limit,18);
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

%Parallelization added by Kassie Povinelli
StatesCell = cellmat(NumIt, 1, 1000, 14);
parfor s=1:NumIt % for every iteration under the same setting
    s %print out s
    %DC code
    States = S_DCPowerFlowSimulation_ANN_dataset(OriginalMPC, NumBranches, NoCoopPercentageVector, StateCounter, TrueCaps, DGRatioVector, WhichInitialLoad, Capacity, s, IniFtable, len_DGRatioVector, len_DeltaVector, DeltaVector, len_NoCoopPercentageVector, FlowCap, DemandIndex);
    %StatesCell(s, 1) = {DCPowerFlowSimulation(OriginalMPC, NumBranches, NoCoopPercentageVector, StateCounter, TrueCaps, DGRatioVector, WhichInitialLoad, Capacity, s, IniFtable, len_DGRatioVector, len_DeltaVector, DeltaVector, len_NoCoopPercentageVector, FlowCap, DemandIndex)};
    %AC code
    &StatesCell(s, 1) = {ACPowerFlowSimulation(OriginalMPC, NumBranches, NoCoopPercentageVector, StateCounter, TrueCaps, DGRatioVector, WhichInitialLoad, Capacity, s, IniFtable, len_DGRatioVector, len_DeltaVector, DeltaVector, len_NoCoopPercentageVector, FlowCap, DemandIndex)};
end
%Temporary -- turn states cell array back to array
States = cell2mat(StatesCell); %Turn cells to states matrix
toc
end