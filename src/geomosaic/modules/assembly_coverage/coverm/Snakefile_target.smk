
rule all_coverm:
    input:
        expand("{wdir}/{sample}/coverm", sample=config["SAMPLES"], wdir=config["WDIR"]),
