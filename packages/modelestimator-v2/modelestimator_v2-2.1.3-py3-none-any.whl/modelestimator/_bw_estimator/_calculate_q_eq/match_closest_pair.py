import numpy as np

### Private functions
def _matching_letters(a,b, COMPARE_INDELS_FLAG):
    if (len(a) != len(b)):
        raise ValueError("Sequences need to be of equal length")

    number_of_matching_positions = 0

    if COMPARE_INDELS_FLAG:
        for x,y in zip(a,b):
            if x == y and x != '-' :
                number_of_matching_positions += 1
    else:
        number_of_matching_positions = np.sum(a==b) # Faster than when indels have to be ignored
                   
    return number_of_matching_positions

### Interface
def choose_close_pairs(sequence_list, COMPARE_INDELS_FLAG):
    '''
    Greedily choose a list of sequence pairs based on sequence identity.
    The objective is to avoid the furthermost pairs and to avoid 
    over-sampling of some sequences and edges (in the underlying tree).

    Returns a list of sequence pairs.
    '''
    indexes_and_matching_letters = []

    for PRIMARY_INDEX, PRIMARY_SEQUENCE in enumerate(sequence_list):
        for SECONDARY_INDEX in range(PRIMARY_INDEX+1, len(sequence_list)):
            SECONDARY_SEQUENCE = sequence_list[SECONDARY_INDEX]
            MATCHING_LETTERS = _matching_letters(PRIMARY_SEQUENCE, SECONDARY_SEQUENCE, COMPARE_INDELS_FLAG)

            INDEXES = (PRIMARY_INDEX, SECONDARY_INDEX)
            INDEX_SCORE_TUPLE = (INDEXES, MATCHING_LETTERS)
            indexes_and_matching_letters.append(INDEX_SCORE_TUPLE)

    indexes_and_matching_letters.sort(key=lambda tup: tup[1], reverse = True)   # Sort on matching letters

    matched_indexes = []
    close_pairs = []
    NUMBER_OF_SEQUENCES = len(sequence_list)

    while (NUMBER_OF_SEQUENCES - len(matched_indexes)) >= 2:
        CURRENT_INDEX_AND_MATCHING_LETTERS_TUPLE = indexes_and_matching_letters.pop(0)
        index1, index2 = CURRENT_INDEX_AND_MATCHING_LETTERS_TUPLE[0]

        if not(index1 in matched_indexes) and not(index2 in matched_indexes):
            matched_indexes.append(index1)
            matched_indexes.append(index2)

            seq1= sequence_list[index1]
            seq2 = sequence_list[index2]
            close_pairs.append((seq1, seq2))

    return close_pairs
