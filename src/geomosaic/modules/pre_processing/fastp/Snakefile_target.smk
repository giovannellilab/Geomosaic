
rule all_fastp:
    input:
        expand("{wdir}/{sample}/fastp", sample=config["SAMPLES"], wdir=config["WDIR"]),
        expand("{wdir}/{sample}/fastp/R1.fastq.gz", sample=config["SAMPLES"], wdir=config["WDIR"]),
        expand("{wdir}/{sample}/fastp/R2.fastq.gz", sample=config["SAMPLES"], wdir=config["WDIR"]),
