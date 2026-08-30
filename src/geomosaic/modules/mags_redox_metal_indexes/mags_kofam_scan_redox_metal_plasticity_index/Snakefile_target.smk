
rule all_mags_kofam_scan_redox_metal_plasticity_index:
    input:
        expand("{wdir}/{sample}/mags_kofam_scan_redox_metal_plasticity_index/gather_OK.txt", sample=config["SAMPLES"], wdir=config["WDIR"]),
