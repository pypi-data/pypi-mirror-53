import numpy as np

### Interface
# Weighting the count matrices.
# PW is a list, with the sum of count matrices weighted by their posterior probability
# for evolutionary distance D.
def matrix_weight(COUNT_MATRIX_LIST, POSTERIOR, DIST_SAMPLES):
    NUMBER_OF_DIST_SAMPLES = len(DIST_SAMPLES)
    PW = np.empty((NUMBER_OF_DIST_SAMPLES, 20, 20))
    
    PW = np.tensordot(POSTERIOR, COUNT_MATRIX_LIST, axes=([0],[0]))
    with np.errstate(invalid='ignore'):  # Suppress warning for division with NaN
        PW /= PW.sum(axis=2,keepdims=True)  # Normalize matrix rows
        
    return PW