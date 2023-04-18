
rule all_pileup:
    input:
        expand("{wdir}/{sample}/pileup", sample=config["SAMPLES"], wdir=config["WDIR"]),
