import argparse
import sys

from modelestimator.version import __version__

from modelestimator._bw_estimator.bw_estimator import bw_estimator
from modelestimator.io import handle_input_file, format_model_output
from modelestimator.bootstrap import bootstrapped_stability, q_bootstrap_estimate



description='''
Infer a amino-acid replacement-rate matrix from one or more protein multisequence
alignments. The output is a rate matrix and an associated steady-state amino-acid
distribution vector.
'''
example_usage='''
Example usage:
    modelestimator -t 0.001 file1.fa file2.fa file3.fa
    modelestimator -b 200 file.fa
'''

def setup_argument_parsing():
    '''
    Create an argument parser.
    '''
    ap = argparse.ArgumentParser(description=description, epilog=example_usage,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('infiles', nargs='+', help="One or more infiles, containing protein multialignments in FASTA format or chosen according to the -f/--format option.")
    ap.add_argument('--version', action='version', version='%(prog)s ' + __version__)
    ap.add_argument('-a', '--application', choices=['iqtree', 'mrbayes', 'octave', 'paml', 'phyml', 'raxml'], default='paml',
                    help="Choose output format to suit the application you want to use for inference. The 'iqtree', 'paml', 'phyml', and 'raxml' options are identical. The 'octave' option is for import into Octave (a MatLab-compatible program) and is presenting the actual Q matrix rather than the R matrix used by PAML/PhyML, etc. Default: %(default)s")
    ap.add_argument('-f', '--format', choices=['fasta', 'clustal', 'nexus', 'phylip', 'stockholm'], default='fasta',
                    help="Specify sequence format of input files. Default: %(default)s")
    # ap.add_argument('-f', '--format', choices=['guess', 'fasta', 'clustal', 'nexus', 'phylip', 'stockholm'], default='guess',
    #                 help="Specify what sequence type to assume. Be specific if the file is not recognized automatically. When reading from stdin, the format is always guessed to be FASTA. Default: %(default)s")
    ap.add_argument('-t', '--threshold', type=float, metavar='T', default=0.001,
                    help="Stop when consecutive iterations do not change by more than T. Default: %(default)g")
    ap.add_argument('-b', '--bootstrap', type=int, metavar='N', default=None,
                    help="Estimate the rate matrix using bootstrapping by computing  N resampled replicates of the input multialignment. For each replicate, a rate matrix is computed. The mean matrix the elementwise standard deviation is returned. Only one infile should be given in this mode.")
    ap.add_argument('-B', '--bootstrapped_quality', type=int, metavar='N', default=None,
                    help="Estimate the quality of the rate matrix estimate using a bootstrap procedure. The multialignment is resampled N times and a Q matrix is computed for each replicate. Then the difference (matrix norm) between rate matrix estimated without resampling and each bootstrapped Q is computed and the mean difference is returned. Only one infile should be given in this mode. Returns bootstrap norm.")
    return ap


def main():
    ap = setup_argument_parsing()
    args = ap.parse_args()

    multialignment_list = []

    for f in args.infiles:
        try:
            multialignment = handle_input_file(f, args.format)
            multialignment_list.append(multialignment)
        except Exception as e:
            print(f'Error reading alignments, file "{f}":', e, file=sys.stderr)
            sys.exit(1)
    try:
        if args.bootstrapped_quality:
            multialignment = multialignment_list[0]
            bootstrap_norm, _ = bootstrapped_stability(args.bootstrapped_quality, args.threshold, multialignment)
            print('Bootstrap norm = ' + str(bootstrap_norm))

        elif args.bootstrap:
            Q, eq, Q_sd, n_failures = q_bootstrap_estimate(multialignment_list, args.threshold, args.bootstrap)
            print('This is, so far, nonsensical output. The R matrix is correct, but it is unclear what the SD matrix is. It is treated as a Q matrix.')
            output_string = format_model_output(Q, eq, args.application)
            output_string += '\n\n' + format_model_output(Q_sd, eq, args.application)
            print(output_string)
            if n_failures > 0:
                print(f'Warning: the bootstrap failed in {n_failures} replicates.')

        else:
            Q, EQ = bw_estimator(args.threshold, multialignment_list)
            output_string = format_model_output(Q, EQ, args.application)
            print(output_string)

    except Exception as e:
        print('Error:', e, file=sys.stderr)
        sys.exit(1)
