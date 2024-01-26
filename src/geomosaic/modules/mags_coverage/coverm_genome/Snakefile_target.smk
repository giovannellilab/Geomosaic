
rule all_coverm_genome:
    input:
        expand("{wdir}/{sample}/coverm_genome", sample=config["SAMPLES"], wdir=config["WDIR"]),
