
rule all_prodigal:
    input:
        expand("{wdir}/{sample}/prodigal", sample=config["SAMPLES"], wdir=config["WDIR"]),
