
rule all_argsoap_custom:
    input:
        expand("{wdir}/{sample}/{argsoap_custom_output_folder}", sample=config["SAMPLES"], wdir=config["WDIR"], argsoap_custom_output_folder=config["CUSTOM_DB"]["argsoap_custom"]["output_folder"]),
