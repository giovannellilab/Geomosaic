
rule all_multi_binners:
    input:
        expand("{wdir}/{sample}/multi_binners", sample=config["SAMPLES"], wdir=config["WDIR"]),
        expand("{wdir}/{sample}/multi_binners/concoct/bins", sample=config["SAMPLES"], wdir=config["WDIR"]),
        expand("{wdir}/{sample}/multi_binners/maxbin2/bins", sample=config["SAMPLES"], wdir=config["WDIR"]),
        expand("{wdir}/{sample}/multi_binners/metabat2/bins", sample=config["SAMPLES"], wdir=config["WDIR"]),
