
rule run_trimgalore:
    input:
        r1="{wdir}/{sample}/R1.fastq.gz",
        r2="{wdir}/{sample}/R2.fastq.gz",
    output:
        dir=directory("{wdir}/{sample}/trimgalore"),
        r1="{wdir}/{sample}/trimgalore/R1.fastq.gz", 
        r2="{wdir}/{sample}/trimgalore/R2.fastq.gz"
    threads: config["threads"]
    conda: config["ENVS"]["trimgalore"]
    params:
        user_params=( lambda x: " ".join(filter(None , yaml.safe_load(open(x, "r"))["trimgalore"])) ) (config["USER_PARAMS"]["trimgalore"]) 
    shell:
        """
        trim_galore {params.user_params} --cores {threads} -o {output.dir} {input.r1} {input.r2}
        mv {output.dir}/R1_val_1.fq.gz {output.r1}
        mv {output.dir}/R2_val_2.fq.gz {output.r2}
        """
