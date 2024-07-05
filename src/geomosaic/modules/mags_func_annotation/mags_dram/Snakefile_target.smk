
rule all_mags_dram:
    input:
        expand("{wdir}/{sample}/mags_dram", sample=config["SAMPLES"], wdir=config["WDIR"]),
