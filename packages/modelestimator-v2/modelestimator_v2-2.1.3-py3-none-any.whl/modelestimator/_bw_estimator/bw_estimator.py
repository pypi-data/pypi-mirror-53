from ._calculate_q_eq.match_closest_pair import choose_close_pairs
from ._calculate_q_eq.create_count_matrices import create_count_matrices
from ._calculate_q_eq.calculate_q_eq import calculate_q_eq

def bw_estimator(threshold, msa_list, compare_indels_flag = False):
    '''
    threshold  -  Decides when to stop iterations
    msa_list   -  A list of alignments 
    compare_indels_flag  -  decides if indels should be included when comparing likeness of sequences

    Returns: a rate matrix and a corresponding steady state distribution on amino acids,
             as estimated with the BW method.
    '''
    aggregated_count_matrix_list = []
    
    for msa in msa_list:
        close_pairs = choose_close_pairs(msa, compare_indels_flag)
        count_matrix_list = create_count_matrices(close_pairs)
        aggregated_count_matrix_list.extend(count_matrix_list)

    Q, eq = calculate_q_eq(aggregated_count_matrix_list, threshold)
    
    return Q, eq

