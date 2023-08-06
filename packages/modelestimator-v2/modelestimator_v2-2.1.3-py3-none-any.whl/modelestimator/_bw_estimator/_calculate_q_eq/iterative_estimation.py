import comp_posterior_JC
import estimate_q
import find_eigens
import matrix_weight
import numpy as np
import simple_estimation

#   Kept for reference

### Interface
def _iterative_estimation(COUNT_MATRIX_LIST, THRESHOLD):
    # These are constant throughout the iterations
    VL, VR, EQ = find_eigens(COUNT_MATRIX_LIST) #   EQ is never changed past this in Octave
    
    # Get a first simple estimate using a Jukes-Cantor model
    distSamples = np.arange(1, 200, 5)
    posterior = comp_posterior_JC(COUNT_MATRIX_LIST, distSamples)
    PW, W = matrix_weight(COUNT_MATRIX_LIST, posterior, distSamplews)
    
    MAX_DIVERGENCE = 100
    Qnew = estimate_q(PW, W, VL, VR, EQ, MAX_DIVERGENCE)
    
    # Use this estimate to as a basis for improvement
    condition = False
    iteration = 0
    dv = []
    MAX_ITERATIONS = 10
    Q = np.matrix((20,20))
    
    while (condition == False):
        iteration += 1
        Q = Qnew
        Qnew, difference = simple_estimation(COUNT_MATRIX_LIST, Q, VL, VR, EQ)
        dv.append(difference)
        
        condition = (iteration >= MAX_ITERATIONS or difference < THRESHOLD)
        
    Q = Qnew
    return Q, EQ, dv