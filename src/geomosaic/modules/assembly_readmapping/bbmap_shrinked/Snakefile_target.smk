
rule all_bbmap:
    input:
        expand("{wdir}/{sample}/bbmap_shrinked", sample=config["SAMPLES"], wdir=config["WDIR"]),
