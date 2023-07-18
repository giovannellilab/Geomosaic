
rule run_prodigal:
    input:
        contig_path=expand("{wdir}/{sample}/{assembly}", assembly=config["assembly"], allow_missing=True),
    output:
        directory("{wdir}/{sample}/prodigal")
    params:
        extra="-p meta",
        quiet="-q"
    run:
        shell("mkdir -p {output}")
        shell("prodigal -i {input.contig_path}/contigs.fasta \
                -o {output}/genes.gff \
                -a {output}/protein_translations.faa \
                -f gff \
                {params.extra} \
                {params.quiet}")

        from geomosaic.parsing_output.prodigal_orf_mapping import parsing_prodigal_orfs

        fasta_input = f"{output}/protein_translations.faa"
        output_mapping = f"{output}/orf_contig_mapping.tsv"
        output_fasta = f"{output}/orf_predicted.faa"
        output_simple_mapping = f"{output}/simple_orf_contig_mapping.tsv"

        parsing_prodigal_orfs(fasta_input, output_mapping, output_fasta, output_simple_mapping)
