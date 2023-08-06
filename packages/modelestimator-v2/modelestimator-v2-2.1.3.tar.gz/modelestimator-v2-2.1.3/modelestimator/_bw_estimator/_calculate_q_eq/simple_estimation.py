from .comp_posterior import comp_posterior
from .matrix_weight import matrix_weight
from .estimate_q import estimate_q

import numpy as np

def simple_estimation(COUNT_MATRIX_LIST, Q_OLD, VL, VR, EQ, DIST_SAMPLES):
    POSTERIOR  = comp_posterior(COUNT_MATRIX_LIST, Q_OLD, EQ, DIST_SAMPLES)
    W = POSTERIOR.sum(axis=0)
    PW = matrix_weight(COUNT_MATRIX_LIST, POSTERIOR, DIST_SAMPLES)
    Q_NEW = estimate_q(PW, W, VL, VR, EQ, DIST_SAMPLES)
    
    return Q_NEW