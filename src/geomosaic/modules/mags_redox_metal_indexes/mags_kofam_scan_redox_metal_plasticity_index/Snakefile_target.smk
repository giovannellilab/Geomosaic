
rule all_mags_kofam_scan_redox_metal_plasticity_index:
    input:
        expand("{wdir}/{sample}/mags_kofam_scan_redox_metal_plasticity_index/gather_OK.txt", sample=config["SAMPLES"], wdir=config["WDIR"]),
        expand("{wdir}/{sample}/mags_kofam_scan_redox_metal_plasticity_index/gather_redox_metal_index_OK.txt", sample=config["SAMPLES"], wdir=config["WDIR"]),