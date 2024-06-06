
rule all_bowtie2_shrinked:
    input:
        expand("{wdir}/{sample}/bowtie2_shrinked", sample=config["SAMPLES"], wdir=config["WDIR"]),
