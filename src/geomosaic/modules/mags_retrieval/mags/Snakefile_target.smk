
rule all_mags:
    input:
        expand("{wdir}/{sample}/mags", sample=config["SAMPLES"], wdir=config["WDIR"]),
