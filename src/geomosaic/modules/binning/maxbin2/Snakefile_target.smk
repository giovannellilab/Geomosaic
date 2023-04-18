
rule all_maxbin2:
    input:
        expand("{wdir}/{sample}/maxbin2", sample=config["SAMPLES"], wdir=config["WDIR"]),
