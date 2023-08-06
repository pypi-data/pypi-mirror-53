import sys
import numpy as np
from Bio import AlignIO

def handle_input_file(file_path, format):
    '''
    Return aligned sequences found in given file.
    Note that the format parameter is a string accepted by AlignIO.read().
    '''
    seq_list = AlignIO.read(file_path, format)
    seq_list = [str(sequence.seq) for sequence in seq_list]

    number_of_sequences = len(seq_list)
    sequence_length = len(seq_list[0])
    new_array = np.empty([number_of_sequences, sequence_length], dtype='U')

    for index, sequence in enumerate(seq_list):
        new_array[index] = np.array(list(sequence))

    return new_array

def format_model_output(Q, eq, out_format):
    if out_format in ['iqtree', 'paml', 'phyml', 'raxml']:
        return paml_model_output(Q, eq)
    elif out_format == 'mrbayes':
        return mrbayes_model_output(Q, eq)
    elif out_format in ['matlab', 'octave']:
        return octave_model_output(Q, eq)

def paml_model_output(Q, eq):
    '''
    Construct and return a string containing the
    R matrix (which is symmetric and q_ij = r_ij*p_j)
    for subsequent use in PAML.
    '''
    output_string = ''
    for row in range(1,20):
        for col in range(0, row):
            r = Q[row, col] / eq[col]
            output_string += f'{r:<8.5} '
        output_string = output_string.rstrip()
        output_string += '\n'

    eq_str = ''
    for elem in range(0,20):
        eq_str += f'{eq[elem]:<8.5} '

    output_string += '\n' + eq_str.rstrip()
    return output_string

def mrbayes_model_output(Q, eq):
    '''
    Output the MrBayes instruction to get user defined rates.

    WARNING: This output is not verified against MrBayes.
    '''
    output_string = 'prset aarevmatpr = fixed('
    rate_list = []
    for row in range(1,20):
        for col in range(0, row):
            r = Q[row, col] / eq[col]
            rate_list.append(f'{r:8.5}')
    output_string += ','.join(rate_list) + ')'
    return output_string

def octave_model_output(Q, eq):
    '''
    Output an Octave-style matrix and vector assigned to 'Q' and a 'eq'.
    NOTE: It is the Q matrix, not the symmetric replacment rates as e.g. PAML
          and PhyML prefers.
    '''
    q_str = '''# name: Q
# type: matrix
# rows: 20
# columns: 20
'''
    for row in Q:
        q_str += '  '.join(map(lambda e: str(round(e, 6)),row))
        q_str += '\n'

    eq_str = '''# name: eq
# type: matrix
# rows: 1
# columns: 20
'''
    eq_str += ' '.join(map(lambda e: str(round(e, 6)), eq))
    return q_str + '\n' + eq_str

# ...but if outputting the R matrix (which is symmetric and q_ij = r_ij*p_j)
# we get compatibility with other tools, like PhyML.
