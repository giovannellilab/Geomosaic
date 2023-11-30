
rule run_metaspades:
    input:
        r1=expand("{wdir}/{sample}/{pre_processing}/R1.fastq.gz", pre_processing=config["pre_processing"], allow_missing=True),
        r2=expand("{wdir}/{sample}/{pre_processing}/R2.fastq.gz", pre_processing=config["pre_processing"], allow_missing=True),
    output:
        directory("{wdir}/{sample}/metaspades")
    threads: 5
    conda: config["ENVS"]["metaspades"]
    params:
        user_params=( lambda x: " ".join(filter(None , yaml.safe_load(open(x, "r"))["metaspades"])) ) (config["USER_PARAMS"]["metaspades"]) 
    shell:
        "spades.py {params.user_params} --meta --only-assembler -t {threads} {params.user_params} -1 {input.r1} -2 {input.r2} -o {output}"


rule run_metaspades_parser:
    input: "{wdir}/{sample}/metaspades"
    output:
        output_fasta="{wdir}/{sample}/metaspades/geomosaic_contigs.fasta",
        output_mapping="{wdir}/{sample}/metaspades/mapping.tsv"
    run:
        contigs_fasta  = os.path.join(str(input), "contigs.fasta")
        
        from geomosaic.parsing_output.rename_contigs import rename_contigs
        rename_contigs(contigs_fasta, output_fasta, output_mapping)
