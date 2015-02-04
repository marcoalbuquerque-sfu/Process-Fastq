import itertools

IUPAC = {'A':['A'],'C':['C'],'G':['G'],'T':['T'],'W':['A','T'],'S':['C','G'],'M':['A','C'],'K':['G','T'],'R':['A','G'],'Y':['C','T'],'B':['C','G','T'],'D':['A','G','T'],'H':['A','C','T'],'V':['A','C','G'],'N':['A','C','G','T']}


### Check if characters in seq are IUPAC nucleotide symbols
def is_iupac( seq ):
    is_seq_iupac = True
    for base in seq:
        is_seq_iupac = is_seq_iupac and base in IUPAC
    return is_seq_iupac


### Determines if seq is ambiguous (all symbols map to a single nucleotide)
def is_unambiguous( seq ):
    is_seq_unambiguous = True
    for base in seq:
        is_seq_unambiguous = is_seq_unambiguous and len(IUPAC[base]) == 1
    return is_seq_unambiguous


### Determines if seq is ambiguous (at least one symbol maps to two nucleotides)
def is_ambiguous( seq ):
    is_seq_ambiguous = False
    for base in seq:
        is_seq_ambiguous = is_seq_ambiguous or not len(IUPAC[base]) == 1
    return is_seq_ambiguous


### Determines logical AND of seq being a subset of ref across all pos
def is_match( seq, ref ):
    is_seq_match = True
    for i in range(0, len(seq)):
        is_seq_match = is_seq_match and set(IUPAC[seq[i]]).issubset(IUPAC[ref[i]])
    return is_seq_match


### Produces all possible strings in order to make seq into ref. 
def make_reference( seq, ref ):
    # If seq[i] is a subset of ref[i], then seq is either more specific
    # or exactly the same as ref, so at position i an unambiguous
    # nucleotide should be from seq[i] 
    # Otherwise seq[i] is not a subset of ref[i], meaning that there
    # exists some mismatches between the unambiguous characters in seq
    # when compared to those in ref, so at position i an unambiguous 
    # nucleotide should be from ref[i]
    nucleotides_lists = []
    for i in range(0, len(seq)):
        if set(IUPAC[seq[i]]).issubset(IUPAC[ref[i]]):
            nucleotides_lists.append(IUPAC[seq[i]])
        else:
            nucleotides_lists.append(IUPAC[ref[i]])
    
    # Converts nucleotide lists into all possible char combinations
    char_lists = itertools.product(*nucleotides_lists)
    
    # Joins the character combinations into their appropriate strigs
    unambiguous_nucleotides =[]
    for chars in char_lists:
        unambiguous_nucleotides.append(''.join(chars))
    
    return unambiguous_nucleotides


### Produces all possible unambiguous nucleotide sequences from seq
def make_unambiguous( seq ):
    # Store all the unambiguous nucleotides in a list for each
    # particular base
    nucleotide_lists = []
    for base in seq:
        nucleotide_lists.append(IUPAC[base])
    # Convert this list into all possible combinations of those
    # characters
    char_lists = itertools.product(*nucleotide_lists)

    # Join the character lists into their appropriate strings
    unambiguous_nucleotides = []
    for chars in char_lists:
        unambiguous_nucleotides.append(''.join(chars))

    return unambiguous_nucleotides