
rule all_mags_kofam_scan:
    input:
        expand("{wdir}/{sample}/mags_kofam_scan/gather_OK.txt", sample=config["SAMPLES"], wdir=config["WDIR"]),
