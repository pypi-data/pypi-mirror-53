import tempfile
import numpy as np
import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from modelestimator._bw_estimator.bw_estimator import bw_estimator
from modelestimator.io import handle_input_file

def test_case_2(tmpdir):
        #   Create directory paths
    CURRENT_DIR = os.path.dirname(__file__)
    TEST_FILES_PATH = os.path.join(CURRENT_DIR, 'test_case_2/')

    #   Create sequence file path
    SEQUENCE_FILE_NAME = "testcase2_20seqs_1000long_50pam.fa"
    FILE_PATH = os.path.join(TEST_FILES_PATH, SEQUENCE_FILE_NAME)

    #   Load reference Q and EQ
    REFERENCE_Q_PATH = os.path.join(TEST_FILES_PATH, 'reference_Q.txt')
    REFERENCE_Q = np.loadtxt(REFERENCE_Q_PATH)
    REFERENCE_EQ_PATH = os.path.join(TEST_FILES_PATH, 'reference_EQ.txt')
    REFERENCE_EQ = np.loadtxt(REFERENCE_EQ_PATH)

    #   Calculate Q and EQ
    FORMAT = "fasta"
    MULTIALIGNMENT = handle_input_file(FILE_PATH, FORMAT)
    MULTLIGNMENT_LIST = [MULTIALIGNMENT]
    THRESHOLD = 0.001
    CALCULATED_Q, CALCULATED_EQ = bw_estimator(THRESHOLD, MULTLIGNMENT_LIST)

    #   Assert that calculated and references are close. Expected to pass
    assert(np.allclose(CALCULATED_Q, REFERENCE_Q, atol=THRESHOLD))
    assert(np.allclose(CALCULATED_EQ, REFERENCE_EQ, atol=THRESHOLD))
