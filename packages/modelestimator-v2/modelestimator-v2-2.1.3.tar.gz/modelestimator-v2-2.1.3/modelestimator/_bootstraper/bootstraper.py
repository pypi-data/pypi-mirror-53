import copy
import random
import numpy as np
import math
import sys
import os

### TO BE DELETED

sys.path.insert(1, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from _bw_estimator.bw_estimator import bw_estimator

#   Private functions
def resample_columns(MULTIALIGNMENT_ARRAY):
    new_multialignment = np.empty_like(MULTIALIGNMENT_ARRAY)
    SEQUENCE_LENGTH = MULTIALIGNMENT_ARRAY.shape[1]

    for COLUMN_INDEX in range(SEQUENCE_LENGTH):
        RANDOM_INDEX = random.randint(0, SEQUENCE_LENGTH - 1)
        new_multialignment[:, COLUMN_INDEX] = MULTIALIGNMENT_ARRAY[:, RANDOM_INDEX]

    return new_multialignment

def calculate_bw_for_resamplings(resamplings, threshold, multialignment):
    q_list = []
    eq_list = []
    number_of_times_bw_estimator_failed = 0

    for _ in range(resamplings):
        resampled_multialignment = resample_columns(multialignment)        
        resampled_multialignment_list = [resampled_multialignment]

        try:
            Q, EQ = bw_estimator(threshold, resampled_multialignment_list)
            q_list.append(Q)
            eq_list.append(EQ)
        except:
            number_of_times_bw_estimator_failed +=1

    failed_percentage = number_of_times_bw_estimator_failed / resamplings
    return q_list, failed_percentage

def q_diff_mean(REFERENCE_Q, RESAMPLED_Q_LIST):
    Q_DIFF_NORM_LIST = []

    for Q in RESAMPLED_Q_LIST:
        Q_DIFF = REFERENCE_Q - Q
        Q_DIFF_NORM = np.linalg.norm(Q_DIFF)
        Q_DIFF_NORM_LIST.append(Q_DIFF_NORM)
    Q_DIFF_MEAN = np.mean(Q_DIFF_NORM_LIST)

    return Q_DIFF_MEAN

def q_bootstrap_estimate(resampled_Q_list):
    '''
    Compute the mean Q matrix and elementwise standard deviations given a list of bootstrap Q
    estimate from resampled alignments.

    Return estimated Q and the std dev as an error estimate.
    '''
    collection = np.stack(resampled_Q_list)
    mean_estimate = np.mean(collection, axis=0) # Corresponds to elementwise mean
    std_dev = np.std(collection, axis=0)        # ...and standard deviation

    return mean_estimate, std_dev


#   Interface
def bootstrapper(resamplings, threshold, multialignment):
    multialignment_list = [multialignment]
    try:
        reference_Q, _ = bw_estimator(threshold, multialignment_list)
    except:
        raise ValueError("Failed to estimate a baseline Q matrix in bootstrap procedure")

    resampled_q_list, failed_percentage = calculate_bw_for_resamplings(resamplings, threshold, multialignment)
    mean_difference = q_diff_mean(reference_Q, resampled_q_list)
    mean_difference *= 10000

    return mean_difference, failed_percentage
