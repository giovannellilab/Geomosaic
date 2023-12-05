
rule all_bbmap:
    input:
        expand("{wdir}/{sample}/bbmap", sample=config["SAMPLES"], wdir=config["WDIR"]),
