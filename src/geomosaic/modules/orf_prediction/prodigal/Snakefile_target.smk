
rule all_prodigal:
    input:
        expand("{wdir}/{sample}/prodigal/orf_predicted.faa", sample=config["SAMPLES"], wdir=config["WDIR"]),
