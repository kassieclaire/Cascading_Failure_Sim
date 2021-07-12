import scipy.io
clusters_matrix_name='cluster_branch_118'
#for IEEE118
number_of_lines=186
#list of lines not represented (include all branch indeces at first)
lines_not_represented=list(range(1,number_of_lines+1))
lines_that_shouldnt_be_represented = []
#extract clusters lists
cluster_mat = scipy.io.loadmat(clusters_matrix_name)
cluster_lists = [l.tolist() for l in cluster_mat[clusters_matrix_name][0]]
clusters = [[item for sublist in cluster_list for item in sublist] for cluster_list in cluster_lists]
#go through branch cluster information and check against indeces of lines that should exist in these clusters
for cluster in clusters:
    for value in cluster:
        if value in lines_not_represented:
            lines_not_represented.remove(value)
        else: #value shoulnd't be in this list -- is either repeat or incorrect index for branches
            lines_that_shouldnt_be_represented.append(value)
if len(lines_not_represented) > 0:
    print("Line indeces that should be represented that aren't: ", lines_not_represented)
if len(lines_that_shouldnt_be_represented) > 0:
    print("Line indeces that shouldn't be represented that are: ", lines_that_shouldnt_be_represented)
