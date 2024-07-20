
from Bio.SeqIO.FastaIO import SimpleFastaParser
from geomosaic._utils import GEOMOSAIC_ERROR


def rename_contigs(contigs_fasta, output_fasta, output_mapping):
    contigs_list = []
    with open(contigs_fasta) as fd:
        for header, seq in SimpleFastaParser(fd):
            contigs_list.append((header, seq))

    if len(contigs_list) == 0:
        print(f"\n{GEOMOSAIC_ERROR}: Your Assembler didn't provide any contigs longer than the minimum length specified. Try to lower these values. SystemExit.\n")
        exit(1)

    with open(output_fasta, "wt") as fo, open(output_mapping, "wt") as fm:
        fm.write("old_header\tnew_header\n")
        for idx, i in enumerate(contigs_list, start = 1):
            old_header, seq = i
            new_header = f"contig_{idx}"
            fo.write(f">{new_header}\n{seq}\n")
            fm.write(f"{old_header}\t{new_header}\n")
