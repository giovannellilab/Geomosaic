
rule all_kofam_scan:
    input:
        expand("{wdir}/{sample}/kofam_scan", sample=config["SAMPLES"], wdir=config["WDIR"]),
