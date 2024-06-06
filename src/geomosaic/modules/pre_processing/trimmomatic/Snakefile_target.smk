
rule all_trimmomatic:
  input:
    expand("{wdir}/{sample}/trimmomatic/R1.fastq.gz", sample=config["SAMPLES"], wdir=config["WDIR"]),
    expand("{wdir}/{sample}/trimmomatic/R2.fastq.gz", sample=config["SAMPLES"], wdir=config["WDIR"]),
