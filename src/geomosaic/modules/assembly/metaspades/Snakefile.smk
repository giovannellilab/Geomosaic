
rule run_metaspades:
    input:
        r1=expand("{wdir}/{sample}/{pre_processing}/R1.fastq.gz", pre_processing=config["MODULES"]["pre_processing"], allow_missing=True),
        r2=expand("{wdir}/{sample}/{pre_processing}/R2.fastq.gz", pre_processing=config["MODULES"]["pre_processing"], allow_missing=True),
    output:
        folder = directory("{wdir}/{sample}/metaspades"),
        contigs_fasta = "{wdir}/{sample}/metaspades/contigs.fasta",
        filtered_fasta = "{wdir}/{sample}/metaspades/filtered_contigs.fasta"
    threads: config["threads"]
    conda: config["ENVS"]["metaspades"]
    params:
        user_params=( lambda x: " ".join(filter(None , yaml.safe_load(open(x, "r"))["metaspades"])) ) (config["USER_PARAMS"]["metaspades"]),
        seqkit_params=( lambda x: " ".join(filter(None , yaml.safe_load(open(x, "r"))["seqkit"])) ) (config["USER_PARAMS"]["metaspades"]) 
    shell:
        """
        mkdir -p {output.folder}

        spades.py {params.user_params} --meta --only-assembler -t {threads} {params.user_params} -1 {input.r1} -2 {input.r2} -o {output.folder}
        seqkit seq {params.seqkit_params} {output.contigs_fasta} -o {output.filtered_fasta}
        """

rule run_metaspades_parser:
    input: 
        filtered_fasta = rules.run_metaspades.output.filtered_fasta
    output:
        output_fasta="{wdir}/{sample}/metaspades/geomosaic_contigs.fasta",
        output_mapping="{wdir}/{sample}/metaspades/mapping.tsv"
    run:
        from geomosaic.parser.rename_contigs import rename_contigs
        rename_contigs(str(input.filtered_fasta), str(output.output_fasta), str(output.output_mapping))
