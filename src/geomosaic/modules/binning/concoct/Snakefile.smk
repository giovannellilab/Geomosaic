
rule run_concoct:
    input:
        folder_readmap=expand("{wdir}/{sample}/{assembly_qc_readmapping}", assembly_qc_readmapping=config["assembly_qc_readmapping"], allow_missing=True),
        contig_path=expand("{wdir}/{sample}/{assembly}", assembly=config["assembly"], allow_missing=True)
    output:
        folder=directory("{wdir}/{sample}/concoct")
    threads: 5
    log: "{wdir}/{sample}/benchmark/concoct.log"
    run:
        shell("mkdir -p {output.folder}/fasta_bins")
        shell("cut_up_fasta.py {input.contig_path}/contigs.fasta -c 10000 -o 0 --merge_last -b {output.folder}/contigs_10K.bed > {output.folder}/contigs_10K.fa")
        shell("concoct_coverage_table.py {output.folder}/contigs_10K.bed {input.folder_readmap}/read_mapping_sorted.bam > {output.folder}/coverage_table.tsv")
        shell("concoct --composition_file {output.folder}/contigs_10K.fa --coverage_file {output.folder}/coverage_table.tsv -b {output.folder}/ >> {log} 2>&1")
        shell("merge_cutup_clustering.py {output.folder}/clustering_gt1000.csv > {output.folder}/clustering_merged.csv")
        shell("extract_fasta_bins.py {input.contig_path}/contigs.fasta {output.folder}/clustering_merged.csv --output_path {output.folder}/fasta_bins")
