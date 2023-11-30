
rule all_mags_prodigal:
    input: 
        expand("{wdir}/{sample}/mags_prodigal/gather_OK.txt", wdir=config["WDIR"], sample=config["SAMPLES"])
