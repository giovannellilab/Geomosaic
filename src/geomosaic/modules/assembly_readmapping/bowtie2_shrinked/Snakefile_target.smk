
rule all_bowtie2:
    input:
        expand("{wdir}/{sample}/bowtie2_shrinked", sample=config["SAMPLES"], wdir=config["WDIR"]),
