
rule run_metaspades:
    input:
        r1=expand("{wdir}/{sample}/{pre_processing}/R1.fastq.gz", pre_processing=config["pre_processing"], allow_missing=True),
        r2=expand("{wdir}/{sample}/{pre_processing}/R2.fastq.gz", pre_processing=config["pre_processing"], allow_missing=True),
    output:
        folder = directory("{wdir}/{sample}/metaspades"),
        contigs_fasta = "{wdir}/{sample}/metaspades/contigs.fasta"
    threads: 5
    conda: config["ENVS"]["metaspades"]
    params:
        user_params=( lambda x: " ".join(filter(None , yaml.safe_load(open(x, "r"))["metaspades"])) ) (config["USER_PARAMS"]["metaspades"]) 
    shell:
        """
        mkdir -p {output.folder}

        spades.py {params.user_params} --meta --only-assembler -t {threads} {params.user_params} -1 {input.r1} -2 {input.r2} -o {output.folder}
        """

rule run_metaspades_parser:
    input: 
        contigs_fasta = rules.run_metaspades.output.contigs_fasta
    output:
        output_fasta="{wdir}/{sample}/metaspades/geomosaic_contigs.fasta",
        output_mapping="{wdir}/{sample}/metaspades/mapping.tsv"
    run:
        from geomosaic.parsing_output.rename_contigs import rename_contigs
        rename_contigs(str(input.contigs_fasta), str(output.output_fasta), str(output.output_mapping))
