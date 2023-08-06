import numpy as np

#   Find the index of the eigenvector corresponding to Q's zero eigenvalue.
#   This is recognized as the row (because we will be looking at the 'right'
#   eigenvectors, not the usual left) with all positive or all negative elements.
def find_zero_eigenvalue_eigenvector(MATRIX):
    ZERO_EIGEN_VECTOR_ARRAY = np.array([(EIGEN_VECTOR, INDEX) for INDEX, EIGEN_VECTOR in enumerate(MATRIX) if all(EIGEN_VECTOR > 0) or all(EIGEN_VECTOR < 0)])

    if (len(ZERO_EIGEN_VECTOR_ARRAY) > 1):
        raise ValueError("More than one candidate for null-vector")
    if (len(ZERO_EIGEN_VECTOR_ARRAY) == 0):
        raise ValueError("No candidate for null-vector!")
        
    EIGEN_VECTOR, INDEX = ZERO_EIGEN_VECTOR_ARRAY[0]

    #   Returns as list to return copy and not reference
    return list(EIGEN_VECTOR), INDEX