
from Bio.SeqIO.FastaIO import SimpleFastaParser


def parsing_prodigal_orfs(fasta_input, output_mapping, output_fasta, output_simple):
    with open(fasta_input) as fd, open(output_mapping, "wt") as fom, open(output_fasta, "wt") as fof, open(output_simple, "wt") as fos:
        fom.write("orf_id\tcontig\tleftmost_coord\trightmost_coord\tstrand\torf_sequence\tpartial\tstart_type\trbs_motif\trbs_spacer\tgc_cont\n")
        fos.write("orf_id\tcontig\n")
        for header, orf_seq in SimpleFastaParser(fd):
            _raw, leftmost_coord, rightmost_coord, strand, coord_info = header.split(" # ")
            contig = "_".join(_raw.split("_")[0:-1])
            
            _id, _partial, _start_type, _rbs_motif, _rbs_spacer, _gc_cont = coord_info.split(";")

            partial     = _partial.split("=")[1]
            start_type  = _start_type.split("=")[1]
            rbs_motif   = _rbs_motif.split("=")[1]
            rbs_spacer  = _rbs_spacer.split("=")[1]
            gc_cont     = _gc_cont.split("=")[1]


            id_orf = f"ORF_{_id.split('=')[1]}"

            fom.write(f"{id_orf}\t{contig}\t{leftmost_coord}\t{rightmost_coord}\t{strand}\t{orf_seq}\t{partial}\t{start_type}\t{rbs_motif}\t{rbs_spacer}\t{gc_cont}\n")
            fos.write(f"{id_orf}\t{contig}\n")
            fof.write(f">{id_orf}\n{orf_seq}\n")
