
rule all_trimgalore:
    input:
        expand("{wdir}/{sample}/trimgalore", sample=config["SAMPLES"], wdir=config["WDIR"]),
        expand("{wdir}/{sample}/trimgalore/R1.fastq.gz", sample=config["SAMPLES"], wdir=config["WDIR"]),
        expand("{wdir}/{sample}/trimgalore/R2.fastq.gz", sample=config["SAMPLES"], wdir=config["WDIR"]),
