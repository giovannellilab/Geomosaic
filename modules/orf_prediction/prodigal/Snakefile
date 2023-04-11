
rule run_prodigal:
    input:
        contig_path=expand("{wdir}/{sample}/{assembly}", assembly=config["assembly"], allow_missing=True),
    output:
        directory("{wdir}/{sample}/prodigal")
    params:
        extra="-p meta",
    run:
        shell("mkdir -p {output}")
        shell("prodigal -i {input.contig_path}/contigs.fasta -o {output}/genes.out -a {output}/protein_translations.faa {params.extra}")
