
rule all_trimmomatic:
  input:
    expand("{wdir}/{sample}/r1_paired.fastq.gz", sample=config["SAMPLES"], wdir=config["WDIR"]),
