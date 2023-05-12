
rule all_hmms_cov:
    input:
        expand("{wdir}/{sample}/hmms_cov", sample=config["SAMPLES"], wdir=config["WDIR"]),
