import tempfile
import numpy as np
import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from modelestimator._bw_estimator.bw_estimator import bw_estimator
from modelestimator.io import handle_input_file

def test_case_3(tmpdir):
        #   Create directory paths
    CURRENT_DIR = os.path.dirname(__file__)
    TEST_FILES_PATH = os.path.join(CURRENT_DIR, 'test_case_3/')

    #   Create sequence file path
    FILE_PATH_1 = os.path.join(TEST_FILES_PATH, "JTT_balancedtree_32sequences_10000long_1.fa")
    FILE_PATH_2 = os.path.join(TEST_FILES_PATH, "JTT_balancedtree_32sequences_10000long_2.fa")
    FILE_PATH_3 = os.path.join(TEST_FILES_PATH, "JTT_balancedtree_32sequences_10000long_3.fa")

    #   Load reference Q and EQ
    REFERENCE_Q_PATH = os.path.join(TEST_FILES_PATH, 'test_case_3_Q.txt')
    REFERENCE_Q = np.loadtxt(REFERENCE_Q_PATH)
    REFERENCE_EQ_PATH = os.path.join(TEST_FILES_PATH, 'test_case_3_EQ.txt')
    REFERENCE_EQ = np.loadtxt(REFERENCE_EQ_PATH)

    #   Calculate Q and EQ
    FILE_PATH_LIST = [FILE_PATH_1, FILE_PATH_2, FILE_PATH_3]
    FORMAT = "fasta"
    MULTIALIGNMENT_LIST = []
    for FILE in FILE_PATH_LIST:
        MULTIALIGNMENT = handle_input_file(FILE, FORMAT)
        MULTIALIGNMENT_LIST.append(MULTIALIGNMENT)
    THRESHOLD = 0.001
    CALCULATED_Q, CALCULATED_EQ = bw_estimator(THRESHOLD, MULTIALIGNMENT_LIST)

    #   Assert that calculated and references are close. Expected to pass
    print(CALCULATED_Q)
    assert(np.allclose(CALCULATED_Q, REFERENCE_Q, atol=THRESHOLD))
    assert(np.allclose(CALCULATED_EQ, REFERENCE_EQ, atol=THRESHOLD))
