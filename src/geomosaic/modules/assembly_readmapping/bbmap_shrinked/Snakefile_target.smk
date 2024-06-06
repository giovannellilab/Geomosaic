
rule all_bbmap_shrinked:
    input:
        expand("{wdir}/{sample}/bbmap_shrinked", sample=config["SAMPLES"], wdir=config["WDIR"]),
