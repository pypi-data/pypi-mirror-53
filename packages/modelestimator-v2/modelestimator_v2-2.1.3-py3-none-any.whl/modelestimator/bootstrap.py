import copy
import random
import numpy as np
import math
import sys
import os

from ._bw_estimator.bw_estimator import bw_estimator
from ._bw_estimator._calculate_q_eq.match_closest_pair import choose_close_pairs
from ._bw_estimator._calculate_q_eq.create_count_matrices import create_count_matrices
from ._bw_estimator._calculate_q_eq.calculate_q_eq import calculate_q_eq

#   Private functions
def resample_columns(multialignment_array):
    new_multialignment = np.empty_like(multialignment_array)
    sequence_length = multialignment_array.shape[1]

    for column_index in range(sequence_length):
        random_index = random.randint(0, sequence_length - 1)
        new_multialignment[:, column_index] = multialignment_array[:, random_index]

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


#   Interface
def bootstrapped_stability(resamplings, threshold, multialignment):
    multialignment_list = [multialignment]
    try:
        reference_Q, _ = bw_estimator(threshold, multialignment_list)
    except:
        raise ValueError("Failed to estimate a baseline Q matrix in bootstrap procedure")

    resampled_q_list, failed_percentage = calculate_bw_for_resamplings(resamplings, threshold, multialignment)
    mean_difference = q_diff_mean(reference_Q, resampled_q_list)
    mean_difference *= 10000

    return mean_difference, failed_percentage


def q_bootstrap_estimate(msa_list, threshold, n_bootstraps, compare_indels_flag=False):
    '''
    Compute the mean Q matrix and elementwise standard deviations from resamplings of an input alignment.

    Return estimated Q and the std dev as an error estimate.
    '''
    resampled_Q_list = []
    mean_eq = None
    n_failures = 0
    for i in range(n_bootstraps):
        try:
            aggregated_count_matrix_list = []
            for msa in msa_list:
                resampled_msa = resample_columns(msa)
                close_pairs = choose_close_pairs(resampled_msa, compare_indels_flag)
                count_matrices = create_count_matrices(close_pairs)
                aggregated_count_matrix_list.extend(count_matrices)
            Q, eq = calculate_q_eq(aggregated_count_matrix_list, threshold)
            resampled_Q_list.append(Q)
            if i > 0:
                mean_eq += eq
            else:
                mean_eq = eq
        except Exception as e:
            print('Bootstrap replicate problem:', str(e))
            n_failures += 1

    failed_percentage = float(n_failures) / n_bootstraps
    if failed_percentage <= 0.25:
        collection = np.stack(resampled_Q_list)
        mean_estimate = np.mean(collection, axis=0) # Corresponds to elementwise mean
        mean_eq = mean_eq / (n_bootstraps - n_failures)
        std_dev = np.std(collection, axis=0)        # ...and standard deviation
        return mean_estimate, mean_eq, std_dev, n_failures
    else:
        raise ValueError(f'Too many failed bootstrap replicate attempts, {n_failures} out of {n_bootstraps} (i.e., {failed_percentage:.2})')

