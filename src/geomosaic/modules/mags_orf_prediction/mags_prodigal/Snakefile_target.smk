
rule all_mags_prodigal:
    input:
        expand("{wdir}/{sample}/mags_prodigal", sample=config["SAMPLES"], wdir=config["WDIR"]),
