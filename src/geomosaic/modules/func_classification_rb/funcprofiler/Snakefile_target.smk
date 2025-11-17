
rule all_funcprofiler:
    input:
        expand("{wdir}/{sample}/funcprofiler", sample=config["SAMPLES"], wdir=config["WDIR"]),
