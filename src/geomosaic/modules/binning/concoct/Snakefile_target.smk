
rule all_concoct:
    input:
        expand("{wdir}/{sample}/concoct", sample=config["SAMPLES"], wdir=config["WDIR"]),
