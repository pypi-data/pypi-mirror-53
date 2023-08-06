import numpy as np
from scipy.stats import binom

### Private functions
def _jc_posterior_ng(COUNT_MATRIX, DIST_SAMPLES):
    MATRIX_SUM = COUNT_MATRIX.sum()
    MATRIX_DIAGONAL_SUM = COUNT_MATRIX.diagonal().sum()
    P = np.exp(- DIST_SAMPLES / 100)
    
    likelihood = binom.pmf(MATRIX_DIAGONAL_SUM, MATRIX_SUM, P)

#   This code is not commented in Octave
#    if (any(isnan(likelihood)))
#      # In case the binomial is tricky to compute, approx with normal distr!
#      likelihood = normpdf(k, tot .* p, tot .* p .* (1 .- p)); 
#    endif
    
    likelihood[0] /= 2
    likelihood[-1] /= 2
    
    POSTERIOR_VEC = likelihood / ( likelihood.sum() * (DIST_SAMPLES[1] - DIST_SAMPLES[0]) )

    return POSTERIOR_VEC    
    
### Interface
def comp_posterior_JC(COUNT_MATRIX_LIST, DIST_SAMPLES):
    NUMBER_OF_COUNT_MATRICES = len(COUNT_MATRIX_LIST)
    NUMBER_OF_DIST_SAMPLES = len(DIST_SAMPLES)
    PD = np.empty((NUMBER_OF_COUNT_MATRICES, NUMBER_OF_DIST_SAMPLES))
    
    PD = np.array([_jc_posterior_ng(COUNT_MATRIX, DIST_SAMPLES) for COUNT_MATRIX in COUNT_MATRIX_LIST])
    return PD
        