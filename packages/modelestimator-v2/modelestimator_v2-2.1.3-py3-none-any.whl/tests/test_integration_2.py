import sys
import os
import io
from contextlib import redirect_stdout
import numpy as np
from modelestimator.main import main

#
# Verify Octave-style output. This test is probably too strict. Should be connected to an Octave process, but cannot
# really demand that from the user.
#

def test_integration_2():
    #   Load REFERENCE_OUTPUT_STRING
    reference_output_string_path = "tests/test_integration_2/reference.txt"
    reference_output_string_path = os.path.join(sys.path[0], reference_output_string_path)

    with open(reference_output_string_path) as text_file:
            REFERENCE_OUTPUT_STRING = text_file.read()

    #   Calculate OUTPUT_STRING
    reference_input_string_path = "/tests/test_integration_2/test_integration_1_20seqs_1000long_50pam.fa"
    reference_input_string_path = sys.path[0] + reference_input_string_path
    sys.argv = ["-", "-f", "fasta", "-a", "octave", reference_input_string_path]

    f = io.StringIO()
    with redirect_stdout(f):
        main()

    OUTPUT_STRING = f.getvalue()

    assert(OUTPUT_STRING == REFERENCE_OUTPUT_STRING)
