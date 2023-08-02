
rule all_mags_gtdbtk:
    input:
        expand("{wdir}/{sample}/mags_gtdbtk", sample=config["SAMPLES"], wdir=config["WDIR"]),
