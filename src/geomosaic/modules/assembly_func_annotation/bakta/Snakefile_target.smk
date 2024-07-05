
rule all_bakta:
    input: 
        expand("{wdir}/{sample}/bakta/bakta_annotation.tsv", sample=config["SAMPLES"], wdir=config["WDIR"]),
