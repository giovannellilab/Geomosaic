
rule all_mags_bakta:
    input: 
        expand("{wdir}/{sample}/mags_bakta/bakta_annotation.tsv", sample=config["SAMPLES"], wdir=config["WDIR"]),
