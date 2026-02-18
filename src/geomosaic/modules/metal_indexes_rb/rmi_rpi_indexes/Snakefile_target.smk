
rule all_rmi_rpi_indexes:
    input:
        expand("{wdir}/{sample}/{rmi_rpi_output_folder}/funprof_output", sample=config["SAMPLES"], wdir=config["WDIR"], rmi_rpi_output_folder=config["CUSTOM_DB"]["rmi_rpi_indexes"]["output_folder"]),expand("{wdir}/{sample}/{rmi_rpi_output_folder}/funprof_output/prefetch_out.csv", sample=config["SAMPLES"], wdir=config["WDIR"], rmi_rpi_output_folder=config["CUSTOM_DB"]["rmi_rpi_indexes"]["output_folder"]), expand("{wdir}/{sample}/rmi_rpi_indexes/redox_metabolic_plasticity_indexes/metal_indexes.tsv"), sample=config["SAMPLES"], wdir=config["WDIR"],
