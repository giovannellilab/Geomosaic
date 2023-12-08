
rule all_bowtie2:
    input:
        expand("{wdir}/{sample}/bowtie2", sample=config["SAMPLES"], wdir=config["WDIR"]),
