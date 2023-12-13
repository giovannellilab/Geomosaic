
rule all_mags:
    input:
        expand("{wdir}/{sample}/mags", sample=config["SAMPLES"], wdir=config["WDIR"]),
        expand("{wdir}/{sample}/mags/MAGs.tsv", sample=config["SAMPLES"], wdir=config["WDIR"]),
