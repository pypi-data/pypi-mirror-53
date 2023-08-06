import numpy as np

### Private functions
def _create_count_matrix(SEQUENCE_PAIRS):
    return_matrix = np.zeros((20,20))
    
    ALPHABET = 'ARNDCQEGHILKMFPSTWYV'
    alphabet_dictionary = {}
    for i, letter in enumerate(ALPHABET):
        alphabet_dictionary[letter] = i
    
    for i,_ in enumerate(SEQUENCE_PAIRS[0]):
        a = SEQUENCE_PAIRS[0][i]
        b = SEQUENCE_PAIRS[1][i]
        
        if a not in ALPHABET or b not in ALPHABET:
            continue
        
        return_matrix[alphabet_dictionary[b]][alphabet_dictionary[a]] = return_matrix[alphabet_dictionary[b]][alphabet_dictionary[a]] + 1
        
    return return_matrix

### Interface
def create_count_matrices(SEQUENCE_PAIRS):
    NUMBER_OF_SEQUENCE_PAIRS = len(SEQUENCE_PAIRS)
    count_matrix_list = np.empty((NUMBER_OF_SEQUENCE_PAIRS, 20, 20))

    count_matrix_list = np.array([_create_count_matrix(SEQUENCE_PAIR) for SEQUENCE_PAIR in SEQUENCE_PAIRS])
    
    return count_matrix_list
