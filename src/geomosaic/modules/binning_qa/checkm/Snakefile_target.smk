
rule all_checkm:
    input:
        expand("{wdir}/{sample}/checkm", sample=config["SAMPLES"], wdir=config["WDIR"]),
        expand("{wdir}/{sample}/MAGs", sample=config["SAMPLES"], wdir=config["WDIR"]),
