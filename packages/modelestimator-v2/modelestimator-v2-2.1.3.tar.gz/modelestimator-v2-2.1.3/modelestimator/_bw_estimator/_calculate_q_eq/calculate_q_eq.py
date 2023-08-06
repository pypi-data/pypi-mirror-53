import os
import sys
import numpy as np
from .comp_posterior_JC import comp_posterior_JC
from .matrix_weight import matrix_weight
from .estimate_q import estimate_q
from .simple_estimation import simple_estimation
from .find_eigens import find_eigens

def calculate_q_eq(COUNT_MATRIX_LIST, THRESHOLD):
    #   VL = Inverse of right eigenvectorts
    #   VR = Right eigenvectors
    #   EQ = Right eigenvector corresponding to zero eigenvalue but normalized so it sums to 1
    VL, VR, EQ = find_eigens(COUNT_MATRIX_LIST)

    #   Get a first simple estimate of Q using a Jukes-Cantor model
    DIST_SAMPLES = np.arange(1, 400, 5)
    POSTERIOR = comp_posterior_JC(COUNT_MATRIX_LIST, DIST_SAMPLES)   # posterior.shape = (10, 80). Rows are identical to Octave but in different order
    PW = matrix_weight(COUNT_MATRIX_LIST, POSTERIOR, DIST_SAMPLES)    
    W = POSTERIOR.sum(axis=0)
    q = estimate_q(PW, W, VL, VR, EQ, DIST_SAMPLES)

    #   Set loop variables
    difference = 1+THRESHOLD
    iterations = 0
    MAX_ITERATIONS = 10
    
    #   Calculate Q
    while (iterations < MAX_ITERATIONS and difference > THRESHOLD):
        iterations += 1
        q_new = simple_estimation(COUNT_MATRIX_LIST, q, VL, VR, EQ, DIST_SAMPLES)
        difference = np.linalg.norm(q_new - q)
        q = q_new
    return q, EQ
