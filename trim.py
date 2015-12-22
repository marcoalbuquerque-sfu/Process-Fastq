import argparse
import printer
import fastq
import nucleotide

if __name__ == '__main__':

    printer.general('TRIM')
    printer.general('Parsing Arguments for trim_fastq.py')	
    desc = "Trim paired-end fastq files that contain an adapter sequence (paste this sequence in QNAME)"
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument(
        "-i", "--input",
        nargs=2,
        required=True,
        help="Takes the file locations of the forward and reverse fastq files from paired end sequencing"
        )
    parser.add_argument(
        "-o", "--output",
        nargs=2,
        required=True,
        help="Takes the file locations to store the trimmed forward and reverse fastq files"
        )
    parser.add_argument(
        "-as", "--adapter_sequence",
        type=str,
        default="WSWSWGACT",
        help="The adapter sequence following IUPAC DNA naming"
        )
    parser.add_argument(
        "-mm", "--max_mismatch",
        type=int,
        default=3,
        help="The maximum number of mismatches to accept in reads when trimming, set to the length of the adapter sequence to filter no reads"
        )
    args = parser.parse_args()

    # Determine Possible Adapters
    ref_adapter = ''.join([args.adapter_sequence, args.adapter_sequence])
    good_adapters = nucleotide.make_unambiguous(ref_adapter)

    # Open Fastq files for reading and writing
    forward_input = fastq.FastqOpen(args.input[0], 'r')
    reverse_input = fastq.FastqOpen(args.input[1], 'r')
    forward_output = fastq.FastqOpen(args.output[0], 'w')
    reverse_output = fastq.FastqOpen(args.output[1], 'w')

    # For each read in the forward and reverse fastq files, trim the adapter, at it to the read id
    # and output this new fastq record to the temprary output fastq
    count = 0
    discard = 0
    printer.trim(count, discard)
    for forward_read in forward_input:
        count = count + 1
        reverse_read = reverse_input.next()
        forward_adapter = forward_read.trim(len(args.adapter_sequence))
        reverse_adapter = reverse_read.trim(len(args.adapter_sequence))
        sequenced_adapter = ''.join([forward_adapter.seq, reverse_adapter.seq]);
        true_adapter = ''.join([args.adapter_sequence, args.adapter_sequence]);
        if nucleotide.distance(sequenced_adapter, true_adapter) > args.max_mismatch:
            discard = discard + 1
            continue
        forward_read.id = ''.join(['@', forward_adapter.seq, reverse_adapter.seq, ':', forward_read.id[1:]])
        reverse_read.id = ''.join(['@', forward_adapter.seq, reverse_adapter.seq, ':', reverse_read.id[1:]])
        forward_output.next(forward_read)
        reverse_output.next(reverse_read)
        if count % 100000 == 0:
            printer.trim(count, discard)
    printer.trim(count, discard)

    # Close Fastq Files
    forward_input.close()
    reverse_input.close()
    forward_output.close()
    reverse_output.close()
