
rule run_metaphlan:
    input:
        r1=expand("{wdir}/{sample}/{pre_processing}/R1.fastq.gz", pre_processing=config["MODULES"]["pre_processing"], allow_missing=True),
        r2=expand("{wdir}/{sample}/{pre_processing}/R2.fastq.gz", pre_processing=config["MODULES"]["pre_processing"], allow_missing=True),
    output:
        directory("{wdir}/{sample}/metaphlan")
    params:
        user_params=( lambda x: " ".join(filter(None , yaml.safe_load(open(x, "r"))["metaphlan"])) ) (config["USER_PARAMS"]["metaphlan"]) 
    threads: config["threads"]
    conda: config["ENVS"]["metaphlan"]
    shell:
        """
        mkdir -p {output}

        metaphlan {input.r1},{input.r2} --bowtie2out {output}/metaphlan.bowtie2.bz2 --nproc {threads} --input_type fastq -o {output}/profiled_metagenome.txt

        metaphlan -t marker_pres_table {output}/metaphlan.bowtie2.bz2 --input_type bowtie2out -o {output}/marker_abundance_table.txt

        metaphlan -t rel_ab_w_read_stats {output}/metaphlan.bowtie2.bz2 --input_type bowtie2out -o {output}/profile_and_estimation.txt
        """
