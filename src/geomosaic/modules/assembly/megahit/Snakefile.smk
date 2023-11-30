
rule run_megahit:
    input:
        r1=expand("{wdir}/{sample}/{pre_processing}/R1.fastq.gz", pre_processing=config["pre_processing"], allow_missing=True),
        r2=expand("{wdir}/{sample}/{pre_processing}/R2.fastq.gz", pre_processing=config["pre_processing"], allow_missing=True),
    output:
        folder = directory("{wdir}/{sample}/megahit"),
        contigs_fasta = "{wdir}/{sample}/megahit/contigs.fasta"
    threads: 10
    conda: config["ENVS"]["megahit"]
    params:
        user_params=( lambda x: " ".join(filter(None , yaml.safe_load(open(x, "r"))["megahit"])) ) (config["USER_PARAMS"]["megahit"]) 
    shell:
        """
        megahit {params.user_params} -t {threads} -1 {input.r1} -2 {input.r2} -o {output.folder}
        mv {output.folder}/final.contigs.fa {output.contigs_fasta}
        """

rule run_megahit_parser:
    input: 
        contigs_fasta = rules.run_megahit.output.contigs_fasta
    output:
        output_fasta="{wdir}/{sample}/megahit/geomosaic_contigs.fasta",
        output_mapping="{wdir}/{sample}/megahit/mapping.tsv"
    run:
        from geomosaic.parsing_output.rename_contigs import rename_contigs
        rename_contigs(str(input.contigs_fasta), str(output.output_fasta), str(output.output_mapping))
