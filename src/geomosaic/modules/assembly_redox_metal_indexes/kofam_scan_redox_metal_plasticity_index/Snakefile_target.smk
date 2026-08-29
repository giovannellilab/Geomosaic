
rule all_kofam_scan_redox_metal_plasticity_index:
    input:
        expand("{wdir}/{sample}/{redox_metal_plasticity_index_output_folder}/kofam_scan_output/.csv", sample=config["SAMPLES"], wdir=config["WDIR"], redox_metal_plasticity_index_output_folder=config["CUSTOM_DB"]["redox_metal_plasticity_index"]["output_folder"]),
        expand("{wdir}/{sample}/{redox_metal_plasticity_index_output_folder}/metabolic_index/redox_metal_indexes.tsv", sample=config["SAMPLES"], wdir=config["WDIR"], redox_metal_plasticity_index_output_folder=config["CUSTOM_DB"]["redox_metal_plasticity_index"]["output_folder"]),
        expand("{wdir}/{sample}/{redox_metal_plasticity_index_output_folder}/metabolic_index/redox_metal_indexes_extended.tsv", sample=config["SAMPLES"], wdir=config["WDIR"], redox_metal_plasticity_index_output_folder=config["CUSTOM_DB"]["redox_metal_plasticity_index"]["output_folder"]),
        