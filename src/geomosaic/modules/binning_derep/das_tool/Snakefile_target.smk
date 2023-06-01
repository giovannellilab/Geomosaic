
rule all_das_tool:
    input:
        expand("{wdir}/{sample}/das_tool", sample=config["SAMPLES"], wdir=config["WDIR"]),
