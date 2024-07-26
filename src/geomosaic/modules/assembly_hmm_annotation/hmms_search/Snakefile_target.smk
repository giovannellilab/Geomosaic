
rule all_hmms_search:
    input:
        expand("{wdir}/{sample}/{assembly_hmmsearch_output_folder}", sample=config["SAMPLES"], wdir=config["WDIR"], assembly_hmmsearch_output_folder=config["ADDITIONAL_PARAM"]["assembly_hmmsearch_output_folder"]),
