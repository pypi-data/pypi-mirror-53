import numpy as np
from scipy.linalg import eig
from .find_zero_eigenvalue_eigenvector import find_zero_eigenvalue_eigenvector

def find_eigens(COUNT_MATRIX_LIST):
    P_SUM = sum(0.5 * (MATRIX + MATRIX.T) for MATRIX in COUNT_MATRIX_LIST)

    # Make every row sum to 1
    ROW_SUMS = np.linalg.norm(P_SUM, axis=1, ord=1, keepdims=1)
    P_SUM = np.divide(P_SUM, ROW_SUMS, out=np.zeros_like(P_SUM), where=ROW_SUMS != 0)   # Only divide where the row sum is non-zero

    try:
        EIGEN_VALUES, VR = eig(P_SUM, left=False, right=True)   #   Calculate eigenvalues and the right eigenvectors of P_SUM
    except ValueError:
        raise ValueError("Unable to calculate eigenvalues")

    if not np.all(np.isreal(EIGEN_VALUES)):
        raise ValueError("An eigenvalue is complex")

    VL = np.linalg.inv(VR)

    EQ,_ = find_zero_eigenvalue_eigenvector(VL)
    EQ /= np.linalg.norm(EQ, ord=1)
    EQ = np.absolute(EQ)

    return VL, VR, EQ