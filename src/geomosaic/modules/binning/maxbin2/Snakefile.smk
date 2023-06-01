
rule run_maxbin2:
    input:
        folder_readmap=expand("{wdir}/{sample}/{assembly_qc_readmapping}", assembly_qc_readmapping=config["assembly_qc_readmapping"], allow_missing=True),
        contig_path=expand("{wdir}/{sample}/{assembly}", assembly=config["assembly"], allow_missing=True)
    output:
        folder=directory("{wdir}/{sample}/maxbin2")
    threads: 5
    run:
        shell("mkdir -p {output.folder}/bins")
        shell("run_MaxBin.pl -contig {input.contig_path}/contigs.fasta -abund {input.folder_readmap}/maxbin2_abundance.txt -thread {threads} -out {output.folder}/output")
        shell("mv {output.folder}/*.fasta {output.folder}/bins/")