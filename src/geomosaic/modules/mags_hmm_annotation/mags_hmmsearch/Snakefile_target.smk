
rule all_mags_hmmsearch:
    input: 
        expand("{wdir}/{sample}/{mags_hmmsearch_output_folder}/gather_OK.txt", wdir=config["WDIR"], sample=config["SAMPLES"], mags_hmmsearch_output_folder=config["ADDITIONAL_PARAM"]["mags_hmmsearch_output_folder"]),
