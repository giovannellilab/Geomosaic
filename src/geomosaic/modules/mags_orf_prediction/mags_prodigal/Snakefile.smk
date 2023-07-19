
rule run_mags_prodigal:
    input:
        mags_folder=expand("{wdir}/{sample}/{mags_retrieval}", mags_retrieval=config["mags_retrieval"], allow_missing=True),
    output:
        directory("{wdir}/{sample}/mags_prodigal")
    params:
        extra="-p meta",
        quiet="-q"
    threads: 1
    run:
        shell("mkdir -p {output}")
        
        import pandas as pd
        from geomosaic.parsing_output.prodigal_orf_mapping import parsing_prodigal_orfs

        df_mags = pd.read_csv(str(os.path.join(str(input.mags_folder), "MAGs.tsv")), sep="\t")
        
        for mag in list(df_mags.MAGs):
            print(f"Computing ORF prediction for {mag}")
            output_folder_mag=str(os.path.join(str(output), mag))

            shell("mkdir -p {output_folder_mag}")
            shell("prodigal -i {input.mags_folder}/fasta/{mag}.fa \
                    -o {output_folder_mag}/genes.gff \
                    -a {output_folder_mag}/protein_translations.faa \
                    -f gff \
                    {params.extra} \
                    {params.quiet}")

            fasta_input = str(os.path.join(output_folder_mag, "protein_translations.faa"))
            output_mapping = str(os.path.join(output_folder_mag, "orf_contig_mapping.tsv"))
            output_fasta = str(os.path.join(output_folder_mag, "orf_predicted.faa"))
            output_simple_mapping = str(os.path.join(output_folder_mag, "simple_orf_contig_mapping.tsv"))

            parsing_prodigal_orfs(fasta_input, output_mapping, output_fasta, output_simple_mapping)
