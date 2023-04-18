
rule all_mifaser:
    input:
        expand("{wdir}/{sample}/mifaser", sample=config["SAMPLES"], wdir=config["WDIR"]),
