
rule run_fastq_readscount:
    input:
        r1=expand("{wdir}/{sample}/{pre_processing}/R1.fastq.gz", pre_processing=config["MODULES"]["pre_processing"], allow_missing=True),
        r2=expand("{wdir}/{sample}/{pre_processing}/R2.fastq.gz", pre_processing=config["MODULES"]["pre_processing"], allow_missing=True),
    output:
        folder = directory("{wdir}/{sample}/fastqc_readscount")
    threads: config["threads"]
    conda: config["ENVS"]["fastqc_readscount"]
    params:
        user_params=( lambda x: " ".join(filter(None , yaml.safe_load(open(x, "r"))["fastqc_readscount"])) ) (config["USER_PARAMS"]["fastqc_readscount"])
    shell:
        """
        mkdir -p {output.folder}

        echo "Performing reads count..."
        t_reads_post=$(echo $(zcat {input.r1} | wc -l)/4 | bc)
        echo "$t_reads_post" > {output.folder}/geomosaic_readscount.txt

        echo "Performing FastQC..."
        fastqc --outdir {output.folder} {input.r1}
        fastqc --outdir {output.folder} {input.r2}
        """
