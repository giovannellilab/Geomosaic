
rule run_prodigal:
    input:
        gm_contigs=expand("{wdir}/{sample}/{assembly}/geomosaic_contigs.fasta", assembly=config["assembly"], allow_missing=True),
    output:
        proteins="{wdir}/{sample}/prodigal/protein_translations.faa",
        genes="{wdir}/{sample}/prodigal/genes.gff",
        folder=directory("{wdir}/{sample}/prodigal")
    params:
        meta="-p meta",
        user_params=( lambda x: " ".join(filter(None , yaml.safe_load(open(x, "r"))["prodigal"])) ) (config["USER_PARAMS"]["prodigal"])
    conda: config["ENVS"]["prodigal"]
    shell:
        """
        mkdir -p {output.folder}
        prodigal -i {input.gm_contigs} \
                -o {output.genes} \
                -a {output.proteins} \
                -f gff \
                {params.meta} \
                {params.user_params}
        """

rule parse_prodigal:
    input:
        protein_fasta=rules.run_prodigal.output.proteins
    output:
        output_mapping = "{wdir}/{sample}/prodigal/orf_contig_mapping.tsv",
        output_fasta = "{wdir}/{sample}/prodigal/orf_predicted.faa",
        output_simple_mapping = "{wdir}/{sample}/prodigal/simple_orf_contig_mapping.tsv", 
    threads: 1
    run:
        from geomosaic.parser.prodigal_orf_mapping import parsing_prodigal_orfs
        parsing_prodigal_orfs(str(input.protein_fasta), str(output.output_mapping), str(output.output_fasta), str(output.output_simple_mapping))
