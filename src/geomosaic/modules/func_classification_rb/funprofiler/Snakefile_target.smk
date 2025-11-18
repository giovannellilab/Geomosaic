
rule all_funprofiler:
    input:
        expand("{wdir}/{sample}/funprofiler", sample=config["SAMPLES"], wdir=config["WDIR"]),
