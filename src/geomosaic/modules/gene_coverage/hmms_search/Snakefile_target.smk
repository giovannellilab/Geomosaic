
rule all_hmms_search:
    input:
        expand("{wdir}/{sample}/hmms_search", sample=config["SAMPLES"], wdir=config["WDIR"]),
