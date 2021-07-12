% The case_118_clusters.mat file contains the custer of buses of IEEE118 grid based on the admitance matrix.
% The cluster is baseed on the 118 buses.
% This script converts the clustering of buses into branches.
A=load('case_118_clusters.mat'); % Loading the .mat file 
mpc=loadcase(case118); % Loading the IEEE118 casefile 
cluster_Branch=zeros(186,6); % Creating and empty array of 186 branches of 6 clusters  

% Separating the 118 buses from the cell to matfiles 
cluster1=cell2mat(A.results118(1)); 
cluster2=cell2mat(A.results118(2));
cluster3=cell2mat(A.results118(3));
cluster4=cell2mat(A.results118(4));
cluster5=cell2mat(A.results118(5));
cluster6=cell2mat(A.results118(6));

% Looping through the branches and assigning them to cluster depending on
% which bus the branch is originating from (1st column of mpc.branch)
for i=1:length(mpc.branch(:,1))
    if ismember(mpc.branch(i,1),cluster1)
        cluster_Branch(i,1)=i;
    elseif ismember(mpc.branch(i,1),cluster2)
        cluster_Branch(i,2)=i;
    elseif ismember(mpc.branch(i,1),cluster3)
        cluster_Branch(i,3)=i;
    elseif ismember(mpc.branch(i,1),cluster4)
        cluster_Branch(i,4)=i;
    elseif ismember(mpc.branch(i,1),cluster5)
        cluster_Branch(i,5)=i;
    else
        cluster_Branch(i,6)=i;  
    end
end

% Creating a cell of the clusters 
cluster_branch_118=cell(1,6);
for j=1:6
    cluster_branch_118{j}=nonzeros(cluster_Branch(:,j));
end

% saving the cell array as matfile
save cluster_branch_118.mat cluster_branch_118
        
        