
rule all_fastqc_readscount:
    input:
        expand("{wdir}/{sample}/fastqc_readscount", sample=config["SAMPLES"], wdir=config["WDIR"]),