
rule all_mags_hmmsearch:
    input: 
        expand("{wdir}/{sample}/mags_hmmsearch/gather_OK.txt", wdir=config["WDIR"], sample=config["SAMPLES"]),
