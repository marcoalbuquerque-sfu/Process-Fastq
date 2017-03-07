#! /usr/bin/env python

# USAGE:
#   See adapter_predict.py for details
#
# DESCRIPTION:
#   Estimates the adapter/barcode sequence used in paired-end sequencing by building a consensus sequence of the first few nucleotides of each read
#
# AUTHOR:
#   Marco Albuquerque (Creator)
#   Christopher Rushton (ckrushto@sfu.ca)

# If not installed or running with python2, this works fine
try:
    import nucleotide
    import fastq
except ImportError:
    # If installed and running in python3
    from ProDuSe import fastq, nucleotide

import argparse
import sys


"""
Processes command line arguments
"""
desc = "Estimates the adapter sequences used in paired (i.e. foward and reverse) fastq files"
parser = argparse.ArgumentParser()
parser.add_argument(
    "-i", "--input",
    metavar="FASTQ",
    nargs=2,
    required=True,
    help="Paired FASTQ files, coresponding to the forward and reverse reads"
    )
parser.add_argument(
    "-m", "--max_adapter_length",
    default=30,
    type=int,
    help="Maximum adapter length [Default: %(default)s]"
    )


def main(args=None):

    if args is None:
        args = parser.parse_args()

    # Check If Input is Gzip and call appropariate FastqOpen
    read = 'r'
    is_input_one_gzipped = args.input[0].endswith(".gz")
    is_input_two_gzipped = args.input[1].endswith(".gz")
    if is_input_one_gzipped and is_input_two_gzipped:
        read = ''.join([read, 'g'])
    elif is_input_one_gzipped or is_input_two_gzipped:
        sys.stderr.write('ERROR: FASTQ files must either be both be gzipped or both uncompressed\n')
        sys.exit(1)

    # Open Fastq files for reading
    forward_input = fastq.FastqOpen(args.input[0], read)
    reverse_input = fastq.FastqOpen(args.input[1], read)

    counts = [[0 for i in range(5)] for j in range(args.max_adapter_length)]

    # Counts the number of nucleotides at each locus in the adapter sequence
    for forward_read in forward_input:
        reverse_read = reverse_input.next()
        for i in range(args.max_adapter_length):
            counts[i][nucleotide.BASE_TO_INDEX[forward_read.seq[i]]] += 1
            counts[i][nucleotide.BASE_TO_INDEX[reverse_read.seq[i]]] += 1

    predicted_seq = ""

    # Obtain a consensus for the adapter sequence
    for i in range(args.max_adapter_length):
        total = float(sum(counts[i][0:4]))
        props = [float(val) / total for val in counts[i][0:4]]
        min_dist = 1
        min_base = ''
        for real_base, real_props in nucleotide.DIST.items():
            new_dist = nucleotide.dist(real_props, props)
            if new_dist < min_dist:
                min_dist = new_dist
                min_base = real_base
        predicted_seq += min_base

    print(predicted_seq + "\n")


if __name__ == "__main__":
    main()
