
rule all_kraken2:
    input:
        expand("{wdir}/{sample}/kraken2", sample=config["SAMPLES"], wdir=config["WDIR"]),
