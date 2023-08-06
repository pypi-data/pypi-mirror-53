import os
import sys
import numpy as np
from Bio import AlignIO

sys.path.insert(1, os.path.abspath(os.path.join(sys.path[0], "..")))
from modelestimator.bootstrap import q_bootstrap_estimate
from modelestimator.io import handle_input_file

def test_bootstrap_1():
    REFERENCE_FILE_PATH = os.path.abspath(os.path.join(sys.path[0], "tests/test_bootstrap_1/1000LongMultialignment.phylip"))
    MULTIALIGNMENT = handle_input_file(REFERENCE_FILE_PATH, "phylip")

    RESAMPLINGS = 25
    THRESHOLD = 0.001
    Q_mean, EQ_mean, Q_SD, n_failures = q_bootstrap_estimate([MULTIALIGNMENT], THRESHOLD, RESAMPLINGS)
    assert n_failures == 0
    assert np.sum(Q_SD) < 190*0.2

test_bootstrap_1()
