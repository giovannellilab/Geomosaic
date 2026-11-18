
rule all_checkm2:
    input:
        expand("{wdir}/{sample}/checkm2", sample=config["SAMPLES"], wdir=config["WDIR"]),
