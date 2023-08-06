import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from modelestimator._bw_estimator.bw_estimator import bw_estimator
from modelestimator.io import handle_input_file

#   Test that bw_estimator works with a multialignment
#   consisting of an odd number of sequences

def test_odd_sequences():
    #   Create directory paths
    CURRENT_DIR = os.path.dirname(__file__)
    FOLDER_DIR = 'test_odd_sequences/'
    TEST_FILES_PATH = os.path.join(CURRENT_DIR, FOLDER_DIR)

    #   Create sequence file path
    SEQUENCE_FILE_NAME = "nad2.fa.pep.aln"
    FILE_PATH = os.path.join(TEST_FILES_PATH, SEQUENCE_FILE_NAME)

    #   Test run
    FORMAT = "fasta"
    MULTIALIGNMENT = handle_input_file(FILE_PATH, FORMAT)
    MULTIALIGNMENT_LIST = [MULTIALIGNMENT]
    THRESHOLD = 0.001
    _,_ = bw_estimator(THRESHOLD, MULTIALIGNMENT_LIST)
