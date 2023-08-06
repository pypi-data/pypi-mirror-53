import numpy as np
from .find_zero_eigenvalue_eigenvector import find_zero_eigenvalue_eigenvector

### Private functions

# Scale Q so that the average mutation rate is 0.01
def scale_q(Q, EQ):
        SCALE_FACTOR = np.dot(EQ, (-np.diag(Q)))

        if(SCALE_FACTOR == 0):
            raise ZeroDivisionError('No Q diagonal cause a problem in estimate_q.py:scale_q')

        Q /= SCALE_FACTOR

        return Q

#   Sometimes, when data is sparse, Q estimates come out with
#   off-diagonal entries being negative. Not good.
def fix_negatives(Q):
    # Replace negative elements with smallest absolute value
    MINIMUM_ELEMENT = np.min(np.abs(Q))
    Q[Q<0] = MINIMUM_ELEMENT
    #   Recalculate diagonal to be negative rowsums
    np.fill_diagonal(Q, 0)
    ROW_SUMS = Q.sum(axis=1)
    np.fill_diagonal(Q, -ROW_SUMS)

    return Q

def recover_q(L, VR, VL):
    Q = 0.01 * (VR @ np.diag(L) @ VL)
    return Q

# Alternative: Estimate eigenvalues of Q using weighted points
#
# The estimated eigenvalues are returned in L
def _weighted_estimate_eigenvals(PW, W, VL, VR, DIST_SAMPLES):
    # The X and Y matrises will contain 20 least-squares problems, one for each eigenvalue
    NUMBER_OF_DIST_SAMPLES = len(DIST_SAMPLES)
    X = np.empty(NUMBER_OF_DIST_SAMPLES, dtype="float64").reshape((80,1))
    Y = np.empty((20, NUMBER_OF_DIST_SAMPLES))

    # Find the eigenvector corresponding to eigenvalue = 1
    _, NULL_VECTOR_INDEX = find_zero_eigenvalue_eigenvector(VL)

    # Gather some datapoints
    for i, DIST_SAMPLE in enumerate(DIST_SAMPLES):
        ELAMBDA = np.diag(VL @ PW[i] @ VR)
        X[i] = (DIST_SAMPLE / 100) * W[i]

        for li in range(20):
            if (li == NULL_VECTOR_INDEX):
                continue

            if (ELAMBDA[li] > 0):    # Skip complex value data points!
                Y[li, i] = np.real(np.log(ELAMBDA[li])) * W[i]
            else:
                X[i] = 0   # No disturbance if set to 0!
                Y[li, i] = 0

    L = np.zeros(20)

    for i,_ in enumerate(L):
        if(i == NULL_VECTOR_INDEX):
            L[i] = 0
        else:
            tempY = Y[i,:].reshape(80,1)
            L[i] = np.linalg.lstsq(X, tempY, rcond = None)[0]

    return L


### Interface
def estimate_q(PW, W, VL, VR, EQ, DIST_SAMPLES):
    L = _weighted_estimate_eigenvals(PW, W, VL, VR, DIST_SAMPLES)

    Q = recover_q(L, VR, VL)
    Q = fix_negatives(Q)
    Q = scale_q(Q, EQ)

    return Q
