
rule all_multi_binners:
    input:
        expand("{wdir}/{sample}/multi_binners", sample=config["SAMPLES"], wdir=config["WDIR"]),
